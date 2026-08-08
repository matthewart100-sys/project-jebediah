from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from collector.document_admission import (
    DocumentAdmissionConflict,
    DocumentAdmissionValidationError,
    DocumentCustodyRuntime,
    DocumentFormat,
    Ed25519ReceiptVerifier,
    SqliteDurableRepository,
    derive_audit_key,
    generate_master_key,
    generate_salt,
    generate_synthetic_signing_key,
    sign_synthetic_receipt,
    synthetic_authorization_policy,
    synthetic_custody_policy,
    synthetic_retention_policy,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _build_runtime(tmp_path: Path):
    master_key = generate_master_key()
    audit_key = derive_audit_key(master_key, generate_salt())
    repository = SqliteDurableRepository(
        runtime_directory=tmp_path,
        master_key=master_key,
        audit_key=audit_key,
        custody_policy=synthetic_custody_policy(),
    )
    signer_key = generate_synthetic_signing_key()
    signer_id = "synthetic-signer-1"
    policy = synthetic_authorization_policy((signer_id,))
    verifier = Ed25519ReceiptVerifier({signer_id: signer_key.public_key()})
    runtime = DocumentCustodyRuntime(
        repository=repository,
        receipt_verifier=verifier,
        authorization_policy=policy,
        retention_policy=synthetic_retention_policy(),
        custody_policy=synthetic_custody_policy(),
        max_admission_bytes=4096,
    )
    return runtime, signer_id, signer_key


def _build_receipt(
    *,
    signer_id: str,
    signer_key,
    now: datetime,
    receipt_id: str,
):
    policy = synthetic_authorization_policy((signer_id,))
    return sign_synthetic_receipt(
        receipt_id=receipt_id,
        organization_domain_id="synthetic-org",
        source_record_id="source-1",
        source_authority_role="Synthetic Authority",
        principal_id="operator-1",
        purpose=policy.required_purpose,
        classification=policy.required_classification,
        allowed_operation=policy.required_operation,
        retention_profile_id="retention-1",
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(minutes=5),
        signer_key_id=signer_id,
        private_key=signer_key,
    )


def _ooxml_payload(required_part: str) -> bytes:
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "<Types />")
        archive.writestr(required_part, "<document />")
    return payload.getvalue()


def test_runtime_admit_stores_verified_pdf_payload(tmp_path: Path):
    now = _now()
    runtime, signer_id, signer_key = _build_runtime(tmp_path)
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-1",
    )

    result = runtime.admit(
        receipt=receipt,
        payload=b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF",
        admission_attempt_id="attempt-1",
        object_id="object-1",
        now=now,
    )

    assert result.record.object_id == "object-1"
    assert result.record.receipt_id == "receipt-1"


@pytest.mark.parametrize(
    ("document_format", "payload"),
    [
        (DocumentFormat.DOCX, _ooxml_payload("word/document.xml")),
        (DocumentFormat.XLSX, _ooxml_payload("xl/workbook.xml")),
        (DocumentFormat.PPTX, _ooxml_payload("ppt/presentation.xml")),
        (DocumentFormat.CSV, b"topic,status\ngovernance,approved\n"),
        (DocumentFormat.TXT, b"Approved organizational evidence\n"),
        (DocumentFormat.MARKDOWN, b"# Approved evidence\n"),
    ],
)
def test_runtime_admits_each_supported_non_pdf_format(
    tmp_path: Path,
    document_format: DocumentFormat,
    payload: bytes,
):
    now = _now()
    runtime, signer_id, signer_key = _build_runtime(tmp_path)
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id=f"receipt-{document_format.value}",
    )

    result = runtime.admit(
        receipt=receipt,
        payload=payload,
        admission_attempt_id=f"attempt-{document_format.value}",
        object_id=f"object-{document_format.value}",
        now=now,
        document_format=document_format,
    )

    assert result.record.object_id == f"object-{document_format.value}"
    assert result.record.receipt_id == f"receipt-{document_format.value}"


def test_runtime_reserves_receipt_before_payload_validation(tmp_path: Path):
    now = _now()
    runtime, signer_id, signer_key = _build_runtime(tmp_path)
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-2",
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="missing_pdf_signature",
    ):
        runtime.admit(
            receipt=receipt,
            payload=b"not-a-pdf",
            admission_attempt_id="attempt-2",
            object_id="object-2",
            now=now,
        )

    with pytest.raises(DocumentAdmissionConflict, match="receipt_already_used"):
        runtime.admit(
            receipt=receipt,
            payload=b"%PDF-1.7\n%%EOF",
            admission_attempt_id="attempt-3",
            object_id="object-3",
            now=now + timedelta(seconds=1),
        )
