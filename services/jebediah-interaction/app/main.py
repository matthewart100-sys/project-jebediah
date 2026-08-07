"""Canonical interaction, admission, promotion, and grounded-question routes."""

from __future__ import annotations

import base64
import binascii
import hashlib
import os
import re
import secrets
import time
import uuid
import zipfile
from io import BytesIO
from pathlib import PurePosixPath
from typing import Annotated, Any
from xml.etree import ElementTree

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .candidate_store import (
    AdmissionCandidate,
    CandidateStoreError,
    get_candidate_store,
)
from .context_builder import build_messages
from .memory_client import retrieve_context, store_promoted_memory
from .ollama_client import generate


MAX_ADMISSION_BYTES = 1_000_000
MAX_DOCX_ENTRIES = 256
MAX_DOCX_UNCOMPRESSED_BYTES = 10_000_000
DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


_allowed_origins = tuple(
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:3000,http://localhost:3000",
    ).split(",")
    if origin.strip()
)

app = FastAPI(title="Jebediah Interaction Gateway", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(_allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class OpenAIChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str | None = None
    messages: list[dict[str, Any]] | None = None
    prompt: str | None = None


class AdmissionRequest(BaseModel):
    source_record_id: str = Field(min_length=1, max_length=200)
    file_name: str = Field(min_length=1, max_length=255)
    media_type: str
    payload_base64: str
    byte_count: int = Field(gt=0, le=MAX_ADMISSION_BYTES)
    workspace_mode: str
    organization_id: str = Field(min_length=1, max_length=200)


class PromotionRequest(BaseModel):
    candidate_id: str
    workspace_mode: str
    organization_id: str


class RejectionRequest(PromotionRequest):
    reason: str = Field(min_length=1, max_length=500)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4_000)
    workspace_mode: str
    organization_id: str


def _require_governed_auth(
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    expected_token = os.getenv("INTERACTION_SERVICE_TOKEN", "")
    if not expected_token:
        raise HTTPException(status_code=503, detail="governed_auth_not_configured")
    scheme, _, token = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(token, expected_token):
        raise HTTPException(status_code=401, detail="governed_auth_required")


def _candidate_id(request: AdmissionRequest, payload: bytes) -> str:
    digest = hashlib.sha256()
    for value in (
        request.organization_id,
        request.workspace_mode,
        request.source_record_id,
    ):
        digest.update(value.encode("utf-8"))
        digest.update(b"\0")
    digest.update(payload)
    return f"candidate-{digest.hexdigest()[:24]}"


def _extract_pdf_text(payload: bytes) -> str:
    if not payload.startswith(b"%PDF-") or b"%%EOF" not in payload[-2048:]:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure")
    try:
        reader = PdfReader(BytesIO(payload), strict=True)
        content = "\n".join(page.extract_text() or "" for page in reader.pages)
    except (PdfReadError, ValueError) as error:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure") from error
    normalized = " ".join(re.findall(r"[A-Za-z0-9][A-Za-z0-9 .,;:()'/-]*", content))
    if not normalized.strip():
        raise HTTPException(status_code=422, detail="pdf_contains_no_extractable_text")
    return normalized.strip()


def _extract_txt_text(payload: bytes) -> str:
    try:
        content = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise HTTPException(status_code=422, detail="txt_must_be_utf8") from error
    if "\x00" in content:
        raise HTTPException(status_code=422, detail="txt_contains_binary_content")
    normalized = " ".join(content.split())
    if not normalized:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return normalized


def _safe_docx_entries(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    entries = archive.infolist()
    if len(entries) > MAX_DOCX_ENTRIES:
        raise HTTPException(status_code=422, detail="docx_resource_limit_exceeded")
    if sum(entry.file_size for entry in entries) > MAX_DOCX_UNCOMPRESSED_BYTES:
        raise HTTPException(status_code=422, detail="docx_resource_limit_exceeded")
    safe_entries: dict[str, zipfile.ZipInfo] = {}
    for entry in entries:
        path = PurePosixPath(entry.filename)
        if path.is_absolute() or ".." in path.parts or entry.flag_bits & 0x1:
            raise HTTPException(status_code=422, detail="invalid_docx_structure")
        safe_entries[entry.filename] = entry
    return safe_entries


def _extract_docx_text(payload: bytes) -> str:
    if not payload.startswith(b"PK"):
        raise HTTPException(status_code=422, detail="invalid_docx_structure")
    try:
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            entries = _safe_docx_entries(archive)
            required = {"[Content_Types].xml", "word/document.xml"}
            if not required.issubset(entries):
                raise HTTPException(status_code=422, detail="invalid_docx_structure")
            lowered_names = {name.lower() for name in entries}
            active_markers = ("vbaproject.bin", "word/activex/", "word/embeddings/")
            if any(
                marker in name
                for name in lowered_names
                for marker in active_markers
            ):
                raise HTTPException(
                    status_code=422,
                    detail="docx_active_content_not_supported",
                )
            for name in entries:
                if name.endswith(".rels"):
                    relationships = archive.read(name)
                    if b'TargetMode="External"' in relationships or b"TargetMode='External'" in relationships:
                        raise HTTPException(
                            status_code=422,
                            detail="docx_external_relationship_not_supported",
                        )
            document_xml = archive.read("word/document.xml")
    except HTTPException:
        raise
    except (KeyError, OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        raise HTTPException(status_code=422, detail="invalid_docx_structure") from error
    if b"<!DOCTYPE" in document_xml or b"<!ENTITY" in document_xml:
        raise HTTPException(status_code=422, detail="invalid_docx_structure")
    try:
        root = ElementTree.fromstring(document_xml)
    except ElementTree.ParseError as error:
        raise HTTPException(status_code=422, detail="invalid_docx_structure") from error
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
    content = " ".join(
        node.text.strip()
        for node in root.iter(namespace)
        if node.text and node.text.strip()
    )
    if not content:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return content


def _admission_format(request: AdmissionRequest) -> str:
    suffix = PurePosixPath(request.file_name).suffix.lower()
    media_type = request.media_type.lower().split(";", 1)[0].strip()
    allowed_media_types = {
        ".pdf": {"application/pdf", "application/octet-stream"},
        ".docx": {DOCX_MEDIA_TYPE, "application/octet-stream"},
        ".txt": {"text/plain", "application/octet-stream"},
    }
    if suffix not in allowed_media_types or media_type not in allowed_media_types[suffix]:
        raise HTTPException(status_code=415, detail="unsupported_document_type")
    return suffix


def _extract_admission_text(request: AdmissionRequest, payload: bytes) -> str:
    document_format = _admission_format(request)
    if document_format == ".pdf":
        return _extract_pdf_text(payload)
    if document_format == ".docx":
        return _extract_docx_text(payload)
    return _extract_txt_text(payload)


def _workspace_memories(
    context: dict[str, Any],
    *,
    organization_id: str,
    workspace_mode: str,
) -> list[dict[str, Any]]:
    memories = context.get("memories")
    if not isinstance(memories, list):
        return []
    eligible: list[dict[str, Any]] = []
    for memory in memories:
        if not isinstance(memory, dict):
            continue
        metadata = memory.get("metadata")
        if not isinstance(metadata, dict):
            continue
        if metadata.get("organization_id") != organization_id:
            continue
        if metadata.get("workspace_mode") != workspace_mode:
            continue
        if metadata.get("governance_state") != "approved":
            continue
        if not str(metadata.get("source_record_id", "")).strip():
            continue
        if not str(metadata.get("candidate_id", "")).strip():
            continue
        eligible.append(memory)
    return eligible


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jebediah-interaction"}


@app.post("/admission/submit")
async def submit_admission(
    request: AdmissionRequest,
    _authorized: None = Depends(_require_governed_auth),
) -> dict[str, Any]:
    try:
        payload = base64.b64decode(request.payload_base64, validate=True)
    except (binascii.Error, ValueError) as error:
        raise HTTPException(status_code=422, detail="payload_base64_invalid") from error
    if len(payload) != request.byte_count:
        raise HTTPException(status_code=422, detail="byte_count_mismatch")
    content = _extract_admission_text(request, payload)
    candidate_id = _candidate_id(request, payload)
    try:
        get_candidate_store().store(
            AdmissionCandidate(
                candidate_id=candidate_id,
                source_record_id=request.source_record_id,
                organization_id=request.organization_id,
                workspace_mode=request.workspace_mode,
                file_name=request.file_name,
                content=content,
            )
        )
    except CandidateStoreError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return {
        "candidate_id": candidate_id,
        "state": "review_pending",
        "reason": "awaiting_human_governance_review",
    }


@app.post("/admission/promote")
async def promote_admission(
    request: PromotionRequest,
    _authorized: None = Depends(_require_governed_auth),
) -> dict[str, Any]:
    try:
        candidate = get_candidate_store().get(request.candidate_id)
    except CandidateStoreError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    if candidate is None:
        raise HTTPException(status_code=404, detail="candidate_not_found")
    if (
        candidate.organization_id != request.organization_id
        or candidate.workspace_mode != request.workspace_mode
    ):
        raise HTTPException(status_code=404, detail="candidate_not_found")
    if candidate.governance_state == "rejected":
        raise HTTPException(status_code=409, detail="candidate_rejected")
    if candidate.promoted_memory_id is not None:
        return {
            "candidate_id": candidate.candidate_id,
            "knowledge_id": candidate.promoted_memory_id,
            "state": "promoted",
        }
    result = await store_promoted_memory(
        content=f"{candidate.file_name}. {candidate.content}",
        source_record_id=candidate.source_record_id,
        candidate_id=candidate.candidate_id,
        organization_id=candidate.organization_id,
        workspace_mode=candidate.workspace_mode,
    )
    if result.get("status") != "stored":
        raise HTTPException(status_code=409, detail="memory_promotion_rejected")
    memory_id = str(result.get("memory_id", "")).strip()
    if not memory_id:
        raise HTTPException(status_code=503, detail="memory_promotion_response_invalid")
    try:
        get_candidate_store().mark_promoted(candidate.candidate_id, memory_id)
    except CandidateStoreError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {
        "candidate_id": candidate.candidate_id,
        "knowledge_id": memory_id,
        "state": "promoted",
    }


@app.post("/admission/reject")
async def reject_admission(
    request: RejectionRequest,
    _authorized: None = Depends(_require_governed_auth),
) -> dict[str, Any]:
    try:
        candidate = get_candidate_store().get(request.candidate_id)
    except CandidateStoreError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    if candidate is None:
        raise HTTPException(status_code=404, detail="candidate_not_found")
    if (
        candidate.organization_id != request.organization_id
        or candidate.workspace_mode != request.workspace_mode
    ):
        raise HTTPException(status_code=404, detail="candidate_not_found")
    try:
        get_candidate_store().mark_rejected(candidate.candidate_id)
    except CandidateStoreError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {
        "candidate_id": candidate.candidate_id,
        "state": "rejected",
        "reason": request.reason,
    }


@app.post("/questions/ask")
async def ask_governed_question(
    request: QuestionRequest,
    _authorized: None = Depends(_require_governed_auth),
) -> dict[str, Any]:
    context = await retrieve_context(
        request.question,
        organization_id=request.organization_id,
        workspace_mode=request.workspace_mode,
        approved_only=True,
    )
    memories = _workspace_memories(
        context,
        organization_id=request.organization_id,
        workspace_mode=request.workspace_mode,
    )
    trace_id = f"trace-{uuid.uuid4()}"
    if not memories:
        return {
            "trace_id": trace_id,
            "state": "insufficient",
            "reason": "no_approved_workspace_evidence",
            "recommended_decision": "Collect or approve relevant evidence before deciding.",
            "citations": [],
        }
    governed_context = {"query": request.question, "memories": memories}
    statement = await generate(build_messages(request.question, governed_context))
    citations = []
    for memory in memories:
        metadata = memory["metadata"]
        citations.append(
            {
                "source_record_id": metadata["source_record_id"],
                "candidate_id": metadata["candidate_id"],
                "organization_id": metadata["organization_id"],
                "workspace_mode": metadata["workspace_mode"],
            }
        )
    return {
        "trace_id": trace_id,
        "state": "grounded",
        "statement": statement,
        "recommended_decision": "Review the cited governed evidence before action.",
        "citations": citations,
    }


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, Any]:
    context = await retrieve_context(request.message)
    response = await generate(build_messages(request.message, context))
    return {"response": response, "context_used": context}


@app.post("/v1/chat/completions")
async def openai_chat_completions(
    request: OpenAIChatCompletionRequest,
) -> dict[str, Any]:
    user_text: str | None = None
    for message in reversed(request.messages or []):
        if message.get("role") == "user" and isinstance(message.get("content"), str):
            user_text = message["content"]
            break
    user_text = user_text or request.prompt
    if not user_text:
        raise HTTPException(status_code=400, detail="no user message provided")
    context = await retrieve_context(user_text)
    response_text = await generate(build_messages(user_text, context))
    return {
        "id": f"jeb-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "jebediah",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {},
    }


@app.get("/v1/models")
def openai_models() -> dict[str, Any]:
    return {
        "object": "list",
        "data": [
            {
                "id": "jebediah",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "project-jebediah",
                "permissions": [],
            }
        ],
    }
