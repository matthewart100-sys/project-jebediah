"""Canonical interaction, admission, promotion, and grounded-question routes."""

from __future__ import annotations

import base64
import binascii
import csv
import hashlib
import os
import re
import secrets
import time
import uuid
import zipfile
from io import BytesIO, StringIO
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
MAX_OOXML_ENTRIES = 512
MAX_OOXML_UNCOMPRESSED_BYTES = 10_000_000
MAX_TABULAR_CELLS = 100_000
DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
XLSX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
PPTX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)
GOVERNED_ANSWER_MAX_TOKENS = 32


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

    reader = PdfReader(BytesIO(payload), strict=True)
    content = "\n".join(page.extract_text() or "" for page in reader.pages)

    normalized = " ".join(
        re.findall(
            r"[A-Za-z0-9][A-Za-z0-9 .,;:()'/-]*",
            content,
        )
    )

    if not normalized.strip():
        raise HTTPException(
            status_code=422,
            detail="pdf_contains_no_extractable_text",
        )

    return normalized.strip()

def _extract_plain_text(payload: bytes, *, format_name: str) -> str:
    try:
        content = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise HTTPException(
            status_code=422,
            detail=f"{format_name}_must_be_utf8",
        ) from error
    if "\x00" in content:
        raise HTTPException(
            status_code=422,
            detail=f"{format_name}_contains_binary_content",
        )
    normalized = " ".join(content.split())
    if not normalized:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return normalized


def _safe_ooxml_parts(
    payload: bytes,
    *,
    format_name: str,
    required_parts: frozenset[str],
) -> dict[str, bytes]:
    invalid_detail = f"invalid_{format_name}_structure"
    if not payload.startswith(b"PK"):
        raise HTTPException(status_code=422, detail=invalid_detail)
    try:
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_OOXML_ENTRIES:
                raise HTTPException(
                    status_code=422,
                    detail=f"{format_name}_resource_limit_exceeded",
                )
            if sum(entry.file_size for entry in entries) > MAX_OOXML_UNCOMPRESSED_BYTES:
                raise HTTPException(
                    status_code=422,
                    detail=f"{format_name}_resource_limit_exceeded",
                )
            entry_names = {entry.filename for entry in entries}
            if not required_parts.issubset(entry_names):
                raise HTTPException(status_code=422, detail=invalid_detail)
            lowered_names = {name.lower() for name in entry_names}
            active_markers = (
                "vbaproject.bin",
                "/activex/",
                "/embeddings/",
                "/oleobjects/",
                "externallinks/",
                "connections.xml",
                "querytables/",
            )
            if any(
                marker in name
                for name in lowered_names
                for marker in active_markers
            ):
                raise HTTPException(
                    status_code=422,
                    detail=f"{format_name}_active_content_not_supported",
                )
            parts: dict[str, bytes] = {}
            for entry in entries:
                path = PurePosixPath(entry.filename)
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or "\\" in entry.filename
                    or entry.flag_bits & 0x1
                ):
                    raise HTTPException(status_code=422, detail=invalid_detail)
                if entry.is_dir():
                    continue
                part = archive.read(entry)
                lowered_part = part.lower()
                if entry.filename.lower().endswith((".xml", ".rels")) and (
                    b"<!doctype" in lowered_part or b"<!entity" in lowered_part
                ):
                    raise HTTPException(status_code=422, detail=invalid_detail)
                if entry.filename.lower().endswith(".rels") and (
                    b'targetmode="external"' in lowered_part
                    or b"targetmode='external'" in lowered_part
                ):
                    raise HTTPException(
                        status_code=422,
                        detail=f"{format_name}_external_relationship_not_supported",
                    )
                parts[entry.filename] = part
            return parts
    except HTTPException:
        raise
    except (
        KeyError,
        NotImplementedError,
        OSError,
        RuntimeError,
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
    ) as error:
        raise HTTPException(status_code=422, detail=invalid_detail) from error


def _xml_root(payload: bytes, *, format_name: str) -> ElementTree.Element:
    try:
        return ElementTree.fromstring(payload)
    except ElementTree.ParseError as error:
        raise HTTPException(
            status_code=422,
            detail=f"invalid_{format_name}_structure",
        ) from error


def _numbered_part_order(name: str) -> tuple[int, str]:
    match = re.search(r"(\d+)(?=\.xml$)", name)
    return (int(match.group(1)) if match else 0, name)


def _extract_docx_text(payload: bytes) -> str:
    parts = _safe_ooxml_parts(
        payload,
        format_name="docx",
        required_parts=frozenset({"[Content_Types].xml", "word/document.xml"}),
    )
    root = _xml_root(parts["word/document.xml"], format_name="docx")
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
    content = " ".join(
        node.text.strip()
        for node in root.iter(namespace)
        if node.text and node.text.strip()
    )
    if not content:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return content


def _extract_xlsx_text(payload: bytes) -> str:
    parts = _safe_ooxml_parts(
        payload,
        format_name="xlsx",
        required_parts=frozenset({"[Content_Types].xml", "xl/workbook.xml"}),
    )
    worksheet_names = sorted(
        (
            name
            for name in parts
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        ),
        key=_numbered_part_order,
    )
    if not worksheet_names:
        raise HTTPException(status_code=422, detail="invalid_xlsx_structure")

    spreadsheet_namespace = (
        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    )
    shared_strings: list[str] = []
    if "xl/sharedStrings.xml" in parts:
        shared_root = _xml_root(parts["xl/sharedStrings.xml"], format_name="xlsx")
        for item in shared_root.iter(f"{spreadsheet_namespace}si"):
            shared_strings.append(
                " ".join(
                    node.text.strip()
                    for node in item.iter(f"{spreadsheet_namespace}t")
                    if node.text and node.text.strip()
                )
            )

    extracted: list[str] = []
    cell_count = 0
    for worksheet_name in worksheet_names:
        root = _xml_root(parts[worksheet_name], format_name="xlsx")
        for cell in root.iter(f"{spreadsheet_namespace}c"):
            cell_count += 1
            if cell_count > MAX_TABULAR_CELLS:
                raise HTTPException(
                    status_code=422,
                    detail="xlsx_resource_limit_exceeded",
                )
            cell_type = cell.attrib.get("t", "")
            value = ""
            if cell_type == "inlineStr":
                value = " ".join(
                    node.text.strip()
                    for node in cell.iter(f"{spreadsheet_namespace}t")
                    if node.text and node.text.strip()
                )
            else:
                value_node = cell.find(f"{spreadsheet_namespace}v")
                raw_value = (
                    value_node.text.strip()
                    if value_node is not None and value_node.text
                    else ""
                )
                if cell_type == "s" and raw_value:
                    try:
                        value = shared_strings[int(raw_value)]
                    except (IndexError, ValueError) as error:
                        raise HTTPException(
                            status_code=422,
                            detail="invalid_xlsx_structure",
                        ) from error
                elif cell_type == "b" and raw_value:
                    value = "true" if raw_value == "1" else "false"
                else:
                    value = raw_value
            normalized = " ".join(value.split())
            if normalized:
                extracted.append(normalized)
    content = " ".join(extracted)
    if not content:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return content


def _extract_pptx_text(payload: bytes) -> str:
    parts = _safe_ooxml_parts(
        payload,
        format_name="pptx",
        required_parts=frozenset(
            {"[Content_Types].xml", "ppt/presentation.xml"}
        ),
    )
    slide_names = sorted(
        (
            name
            for name in parts
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        ),
        key=_numbered_part_order,
    )
    if not slide_names:
        raise HTTPException(status_code=422, detail="invalid_pptx_structure")
    text_namespace = "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
    extracted: list[str] = []
    for slide_name in slide_names:
        root = _xml_root(parts[slide_name], format_name="pptx")
        extracted.extend(
            node.text.strip()
            for node in root.iter(text_namespace)
            if node.text and node.text.strip()
        )
    content = " ".join(extracted)
    if not content:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return content


def _extract_csv_text(payload: bytes) -> str:
    try:
        content = payload.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise HTTPException(status_code=422, detail="csv_must_be_utf8") from error
    if "\x00" in content:
        raise HTTPException(status_code=422, detail="csv_contains_binary_content")
    extracted: list[str] = []
    cell_count = 0
    try:
        for row in csv.reader(StringIO(content, newline=""), strict=True):
            normalized_row: list[str] = []
            for cell in row:
                cell_count += 1
                if cell_count > MAX_TABULAR_CELLS:
                    raise HTTPException(
                        status_code=422,
                        detail="csv_resource_limit_exceeded",
                    )
                normalized = " ".join(cell.split())
                if normalized:
                    normalized_row.append(normalized)
            if normalized_row:
                extracted.append(" | ".join(normalized_row))
    except csv.Error as error:
        raise HTTPException(status_code=422, detail="invalid_csv_structure") from error
    result = " ".join(extracted)
    if not result:
        raise HTTPException(status_code=422, detail="document_contains_no_extractable_text")
    return result


def _admission_format(request: AdmissionRequest) -> str:
    suffix = PurePosixPath(request.file_name).suffix.lower()
    media_type = request.media_type.lower().split(";", 1)[0].strip()
    allowed_media_types = {
        ".pdf": {"application/pdf", "application/octet-stream"},
        ".docx": {DOCX_MEDIA_TYPE, "application/octet-stream"},
        ".xlsx": {XLSX_MEDIA_TYPE, "application/octet-stream"},
        ".pptx": {PPTX_MEDIA_TYPE, "application/octet-stream"},
        ".csv": {
            "text/csv",
            "application/csv",
            "application/vnd.ms-excel",
            "text/plain",
            "application/octet-stream",
        },
        ".txt": {"text/plain", "application/octet-stream"},
        ".md": {"text/markdown", "text/x-markdown", "text/plain", "application/octet-stream"},
        ".markdown": {
            "text/markdown",
            "text/x-markdown",
            "text/plain",
            "application/octet-stream",
        },
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
    if document_format == ".xlsx":
        return _extract_xlsx_text(payload)
    if document_format == ".pptx":
        return _extract_pptx_text(payload)
    if document_format == ".csv":
        return _extract_csv_text(payload)
    if document_format in {".md", ".markdown"}:
        return _extract_plain_text(payload, format_name="markdown")
    return _extract_plain_text(payload, format_name="txt")


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
        payload = base64.b64decode(
            request.payload_base64,
            validate=True,
        )
    except (binascii.Error, ValueError) as error:
        raise HTTPException(
            status_code=422,
            detail="payload_base64_invalid",
        ) from error

    if len(payload) != request.byte_count:
        raise HTTPException(
            status_code=422,
            detail="byte_count_mismatch",
        )

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
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

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
    messages = build_messages(request.question, governed_context)
    messages[0]["content"] += " Reply with one brief, complete sentence."
    statement = await generate(
        messages,
        max_output_tokens=GOVERNED_ANSWER_MAX_TOKENS,
    )
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
