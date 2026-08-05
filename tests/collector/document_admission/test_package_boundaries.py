import ast
import inspect
from dataclasses import fields, is_dataclass
from pathlib import Path

import collector.document_admission as package
import collector.document_admission.models as model_module
from collector.document_admission import (
    AdmissionAttemptRecord,
    ByteIntegrityVerifier,
    ConsumerEligibilityEvaluator,
    DocumentAdmissionOrchestrator,
    EvidenceJournal,
    FormatDetector,
    InspectionResult,
    IsolatedInspector,
    Phase3BDocumentAdmissionRuntime,
    PolicyEvaluator,
    QuarantineRepository,
    SecurityEvaluator,
    SourceAuthorizationVerifier,
    SubmissionEnvelope,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "src" / "collector" / "document_admission"
TESTS = ROOT / "tests" / "collector" / "document_admission"
SOURCE_MANIFEST = {
    "__init__.py",
    "authorization.py",
    "crypto.py",
    "durable_repository.py",
    "failures.py",
    "in_memory_adapters.py",
    "interfaces.py",
    "lifecycle.py",
    "models.py",
    "orchestration.py",
    "pdf_pipeline.py",
    "policies.py",
    "review.py",
    "runtime.py",
    "state_transitions.py",
}
TEST_MANIFEST = {
    "__init__.py",
    "synthetic_fixtures.py",
    "test_authorization.py",
    "test_models.py",
    "test_policies.py",
    "test_state_transitions.py",
    "test_byte_integrity.py",
    "test_quarantine.py",
    "test_format_detection.py",
    "test_security_dispositions.py",
    "test_resource_limits.py",
    "test_inspection_results.py",
    "test_admission_orchestration.py",
    "test_crypto.py",
    "test_durable_repository.py",
    "test_failure_and_retry.py",
    "test_cleanup.py",
    "test_lifecycle.py",
    "test_package_boundaries.py",
    "test_pdf_pipeline.py",
    "test_review.py",
}


def source_trees():
    for path in SOURCE.glob("*.py"):
        yield path, ast.parse(path.read_text(encoding="utf-8"))


def test_exact_authorized_source_and_test_manifests_exist():
    assert {path.name for path in SOURCE.glob("*.py")} == SOURCE_MANIFEST
    assert {path.name for path in TESTS.glob("*.py")} == TEST_MANIFEST


def test_runtime_package_uses_standard_library_and_relative_imports_only():
    allowed_roots = {
        "abc",
        "__future__",
        "base64",
        "collections",
        "dataclasses",
        "datetime",
        "enum",
        "hashlib",
        "hmac",
        "json",
        "os",
        "pathlib",
        "re",
        "sqlite3",
        "typing",
        "cryptography",
    }
    for path, tree in source_trees():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert {
                    alias.name.partition(".")[0] for alias in node.names
                } <= allowed_roots, path
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                assert node.module.partition(".")[0] in allowed_roots, path


def test_runtime_package_has_no_execution_or_io_calls():
    prohibited_calls = {
        "__import__",
        "compile",
        "eval",
        "exec",
        "input",
        "open",
    }
    for path, tree in source_trees():
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
        }
        assert called_names.isdisjoint(prohibited_calls), path


def test_runtime_package_has_no_prohibited_integration_terms():
    prohibited = {
        "docker",
        "embedding",
        "fastapi",
        "n8n",
        "ollama",
        "qdrant",
        "requests",
        "socket",
        "subprocess",
    }
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in SOURCE.glob("*.py")
    )
    assert prohibited.isdisjoint(combined.split())


def test_all_external_behavior_contracts_remain_abstract():
    contracts = (
        ByteIntegrityVerifier,
        QuarantineRepository,
        EvidenceJournal,
        FormatDetector,
        SecurityEvaluator,
        PolicyEvaluator,
        IsolatedInspector,
        ConsumerEligibilityEvaluator,
        DocumentAdmissionOrchestrator,
        SourceAuthorizationVerifier,
        Phase3BDocumentAdmissionRuntime,
    )
    assert all(inspect.isabstract(contract) for contract in contracts)


def test_models_contain_no_source_body_or_extracted_text_fields():
    prohibited = {
        "body",
        "content",
        "document_bytes",
        "extracted_text",
        "payload",
        "raw_output",
    }
    records = tuple(
        candidate
        for candidate in vars(model_module).values()
        if isinstance(candidate, type)
        and is_dataclass(candidate)
        and candidate.__module__ == model_module.__name__
    )
    for record in records:
        assert prohibited.isdisjoint(
            field.name for field in fields(record)
        )


def test_existing_source_does_not_import_document_admission():
    for path in (ROOT / "src").rglob("*.py"):
        if SOURCE in path.parents:
            continue
        assert "collector.document_admission" not in path.read_text(
            encoding="utf-8"
        ), path


def test_public_package_grants_no_runtime_or_truth_authority():
    prohibited_exports = {
        "MemoryItem",
        "PersistentRegistry",
        "ExternalVectorStore",
        "RuntimeService",
        "TruthAuthority",
        "approve",
        "deploy",
        "ingest",
        "promote",
    }
    assert prohibited_exports.isdisjoint(vars(package))


def test_fixture_payloads_are_generated_synthetic_values():
    fixture_text = (
        TESTS / "synthetic_fixtures.py"
    ).read_text(encoding="utf-8")
    assert "SYNTHETIC" in fixture_text
