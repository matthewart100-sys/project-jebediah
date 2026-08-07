from __future__ import annotations

import asyncio
import base64
import zipfile
from io import BytesIO
from pathlib import Path

import httpx
import pytest

from app import candidate_store, main, memory_client
from cryptography.fernet import Fernet


@pytest.fixture(autouse=True)
def _governed_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INTERACTION_SERVICE_TOKEN", "synthetic-service-token")


AUTH_HEADERS = {"Authorization": "Bearer synthetic-service-token"}


def _pdf_bytes(text: str) -> bytes:
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
        ),
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    payload = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{number} 0 obj\n".encode("ascii"))
        payload.extend(body)
        payload.extend(b"\nendobj\n")
    xref_offset = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(payload)


def test_promoted_memory_uses_candidate_derived_idempotency_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[tuple[str, dict[str, object]]] = []

    async def fake_post(path: str, payload: dict[str, object]):
        requests.append((path, payload))
        return {"status": "stored", "memory_id": payload["memory_id"]}

    monkeypatch.setattr(memory_client, "_post", fake_post)

    result = asyncio.run(
        memory_client.store_promoted_memory(
            content="Governed evidence.",
            source_record_id="source-001",
            candidate_id="candidate-001",
            organization_id="virginia-b-andes",
            workspace_mode="development",
        )
    )

    assert result["memory_id"] == "governed-candidate-001"
    assert requests[0][1]["memory_id"] == "governed-candidate-001"


PDF = _pdf_bytes(
    "SYNTHETIC RELEASE EVIDENCE: Board approved the reserve reconciliation plan."
)


def _docx_bytes(text: str) -> bytes:
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '</Types>',
        )
        archive.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body>'
            '</w:document>',
        )
    return output.getvalue()


@pytest.fixture(autouse=True)
def isolated_candidate_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    store = candidate_store.CandidateStore(
        tmp_path / "interaction-state.sqlite3",
        Fernet.generate_key().decode("ascii"),
    )
    monkeypatch.setattr(candidate_store, "_candidate_store", store)


def _admission_payload(**changes):
    payload = {
        "source_record_id": "source-release-001",
        "file_name": "release-evidence.pdf",
        "media_type": "application/pdf",
        "payload_base64": base64.b64encode(PDF).decode("ascii"),
        "byte_count": len(PDF),
        "workspace_mode": "development",
        "organization_id": "virginia-b-andes",
    }
    payload.update(changes)
    return payload


def test_admission_promotion_and_grounded_question_preserve_workspace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stored_payloads: list[dict[str, object]] = []

    async def fake_store(**payload):
        stored_payloads.append(payload)
        return {"status": "stored", "memory_id": "memory-release-001"}

    async def fake_context(_query: str, **_filters):
        return {
            "memories": [
                {
                    "score": 0.91,
                    "content": "Board approved the reserve reconciliation plan.",
                    "metadata": {
                        "candidate_id": candidate_id,
                        "source_record_id": "source-release-001",
                        "organization_id": "virginia-b-andes",
                        "workspace_mode": "development",
                        "governance_state": "approved",
                    },
                },
                {
                    "score": 0.99,
                    "content": "Other organization evidence.",
                    "metadata": {
                        "candidate_id": "candidate-other",
                        "source_record_id": "source-other",
                        "organization_id": "other-organization",
                        "workspace_mode": "development",
                        "governance_state": "approved",
                    },
                },
            ]
        }

    async def fake_generate(_messages):
        return "Leadership should execute the approved reserve reconciliation plan."

    monkeypatch.setattr(main, "store_promoted_memory", fake_store)
    monkeypatch.setattr(main, "retrieve_context", fake_context)
    monkeypatch.setattr(main, "generate", fake_generate)

    async def exercise() -> None:
        nonlocal candidate_id
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            admission = await client.post(
                "/admission/submit",
                json=_admission_payload(),
            )
            assert admission.status_code == 200
            candidate_id = admission.json()["candidate_id"]
            assert admission.json()["state"] == "review_pending"

            promotion = await client.post(
                "/admission/promote",
                json={
                    "candidate_id": candidate_id,
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                },
            )
            assert promotion.status_code == 200
            assert promotion.json()["state"] == "promoted"

            answer = await client.post(
                "/questions/ask",
                json={
                    "question": "What should leadership do next?",
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                },
            )
            assert answer.status_code == 200
            assert answer.json()["state"] == "grounded"
            assert answer.json()["citations"] == [
                {
                    "candidate_id": candidate_id,
                    "source_record_id": "source-release-001",
                    "organization_id": "virginia-b-andes",
                    "workspace_mode": "development",
                }
            ]

    candidate_id = ""
    asyncio.run(exercise())
    assert stored_payloads[0]["organization_id"] == "virginia-b-andes"
    assert stored_payloads[0]["workspace_mode"] == "development"


def test_question_excludes_other_workspace_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_context(_query: str, **_filters):
        return {
            "memories": [
                {
                    "score": 0.99,
                    "content": "Production-only evidence.",
                    "metadata": {
                        "candidate_id": "candidate-production",
                        "source_record_id": "source-production",
                        "organization_id": "virginia-b-andes",
                        "workspace_mode": "production",
                        "governance_state": "approved",
                    },
                }
            ]
        }

    async def fail_generate(_messages):
        raise AssertionError("generation must not run without eligible evidence")

    monkeypatch.setattr(main, "retrieve_context", fake_context)
    monkeypatch.setattr(main, "generate", fail_generate)

    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            answer = await client.post(
                "/questions/ask",
                json={
                    "question": "What should leadership do next?",
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                },
            )
            assert answer.status_code == 200
            assert answer.json()["state"] == "insufficient"
            assert answer.json()["citations"] == []

    asyncio.run(exercise())


def test_admission_rejects_invalid_pdf() -> None:
    invalid = b"not a pdf"

    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            response = await client.post(
                "/admission/submit",
                json=_admission_payload(
                    payload_base64=base64.b64encode(invalid).decode("ascii"),
                    byte_count=len(invalid),
                ),
            )
            assert response.status_code == 422
            assert response.json()["detail"] == "invalid_pdf_structure"

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("file_name", "media_type", "payload", "expected_text"),
    [
        (
            "governed-evidence.txt",
            "text/plain",
            b"Governance committee approved the synthetic plan.",
            "Governance committee approved the synthetic plan.",
        ),
        (
            "governed-evidence.docx",
            main.DOCX_MEDIA_TYPE,
            _docx_bytes("Board approved the synthetic DOCX evidence."),
            "Board approved the synthetic DOCX evidence.",
        ),
    ],
)
def test_txt_and_docx_enter_the_existing_governed_candidate_store(
    file_name: str,
    media_type: str,
    payload: bytes,
    expected_text: str,
) -> None:
    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            response = await client.post(
                "/admission/submit",
                json=_admission_payload(
                    file_name=file_name,
                    media_type=media_type,
                    payload_base64=base64.b64encode(payload).decode("ascii"),
                    byte_count=len(payload),
                ),
            )
            assert response.status_code == 200
            result = response.json()
            assert result["state"] == "review_pending"
            candidate = candidate_store.get_candidate_store().get(result["candidate_id"])
            assert candidate is not None
            assert expected_text in candidate.content

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("file_name", "media_type"),
    [
        ("archive.zip", "application/zip"),
        ("image.png", "image/png"),
        ("mismatch.pdf", "text/plain"),
    ],
)
def test_unsupported_and_mismatched_document_types_are_rejected(
    file_name: str,
    media_type: str,
) -> None:
    payload = b"unsupported synthetic payload"

    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            response = await client.post(
                "/admission/submit",
                json=_admission_payload(
                    file_name=file_name,
                    media_type=media_type,
                    payload_base64=base64.b64encode(payload).decode("ascii"),
                    byte_count=len(payload),
                ),
            )
            assert response.status_code == 415
            assert response.json()["detail"] == "unsupported_document_type"

    asyncio.run(exercise())


def test_duplicate_submission_is_idempotently_governed() -> None:
    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            first = await client.post("/admission/submit", json=_admission_payload())
            duplicate = await client.post("/admission/submit", json=_admission_payload())
            assert first.status_code == duplicate.status_code == 200
            assert first.json()["candidate_id"] == duplicate.json()["candidate_id"]
            assert duplicate.json()["state"] == "review_pending"

    asyncio.run(exercise())


def test_governed_routes_require_service_authentication() -> None:
    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
        ) as client:
            response = await client.post(
                "/admission/submit",
                json=_admission_payload(),
            )
            assert response.status_code == 401
            assert response.json()["detail"] == "governed_auth_required"

    asyncio.run(exercise())


def test_rejected_candidate_cannot_be_promoted() -> None:
    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            admission = await client.post(
                "/admission/submit",
                json=_admission_payload(source_record_id="source-rejected"),
            )
            candidate_id = admission.json()["candidate_id"]
            rejection = await client.post(
                "/admission/reject",
                json={
                    "candidate_id": candidate_id,
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                    "reason": "evidence_insufficient",
                },
            )
            assert rejection.status_code == 200
            assert rejection.json()["state"] == "rejected"
            promotion = await client.post(
                "/admission/promote",
                json={
                    "candidate_id": candidate_id,
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                },
            )
            assert promotion.status_code == 409
            assert promotion.json()["detail"] == "candidate_rejected"

    asyncio.run(exercise())


def test_question_excludes_approved_evidence_without_citation_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_context(_query: str, **_filters):
        return {
            "memories": [
                {
                    "content": "Incomplete approved evidence.",
                    "metadata": {
                        "organization_id": "virginia-b-andes",
                        "workspace_mode": "development",
                        "governance_state": "approved",
                    },
                }
            ]
        }

    async def fail_generate(_messages):
        raise AssertionError("generation must not run without citable evidence")

    monkeypatch.setattr(main, "retrieve_context", fake_context)
    monkeypatch.setattr(main, "generate", fail_generate)

    async def exercise() -> None:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://synthetic.test",
            headers=AUTH_HEADERS,
        ) as client:
            answer = await client.post(
                "/questions/ask",
                json={
                    "question": "What should leadership do next?",
                    "workspace_mode": "development",
                    "organization_id": "virginia-b-andes",
                },
            )
            assert answer.status_code == 200
            assert answer.json()["state"] == "insufficient"

    asyncio.run(exercise())


def test_candidate_custody_is_encrypted_and_survives_store_reopen(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "durable-state.sqlite3"
    key = Fernet.generate_key().decode("ascii")
    store = candidate_store.CandidateStore(database_path, key)
    candidate = candidate_store.AdmissionCandidate(
        candidate_id="candidate-durable",
        source_record_id="source-durable",
        organization_id="synthetic-organization",
        workspace_mode="development",
        file_name="durable.pdf",
        content="Sensitive synthetic candidate text.",
    )
    store.store(candidate)

    assert b"Sensitive synthetic candidate text." not in database_path.read_bytes()
    reopened = candidate_store.CandidateStore(database_path, key)
    assert reopened.get(candidate.candidate_id) == candidate
