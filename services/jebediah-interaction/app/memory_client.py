"""HTTP adapter for the canonical memory service."""
from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import HTTPException


MEMORY_URL = os.getenv("MEMORY_URL", "http://jebediah-memory:8000").rstrip("/")


async def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{MEMORY_URL}{path}",
                json=payload,
            )
            response.raise_for_status()
            decoded = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(
            status_code=503,
            detail="memory service unavailable",
        ) from error

    if not isinstance(decoded, dict):
        raise HTTPException(
            status_code=503,
            detail="memory service response invalid",
        )

    return decoded


async def retrieve_context(
    query: str,
    *,
    organization_id: str | None = None,
    workspace_mode: str | None = None,
    approved_only: bool = False,
) -> dict[str, Any]:
    return await _post(
        "/memory/context",
        {
            "source_identity": "interaction-gateway",
            "content": query,
            "memory_type": "context",
            "importance": 0.5,
            "organization_id": organization_id,
            "workspace_mode": workspace_mode,
            "approved_only": approved_only,
        },
    )


async def store_promoted_memory(
    *,
    content: str,
    source_record_id: str,
    candidate_id: str,
    organization_id: str,
    workspace_mode: str,
) -> dict[str, Any]:
    return await _post(
        "/memory/store",
        {
            "memory_id": f"governed-{candidate_id}",
            "source_identity": source_record_id,
            "content": content,
            "memory_type": "decision",
            "importance": 0.95,
            "provenance": {
                "source": "governed_document_admission",
                "creator": "knowledge-reviewer",
                "creation_context": "human_governance_promotion",
                "confidence_basis": "human_approved_document_admission",
                "verification_state": "verified",
                "supporting_evidence": [
                    candidate_id,
                    source_record_id,
                ],
            },
            "metadata": {
                "candidate_id": candidate_id,
                "source_record_id": source_record_id,
                "organization_id": organization_id,
                "workspace_mode": workspace_mode,
                "governance_state": "approved",
            },
        },
    )
