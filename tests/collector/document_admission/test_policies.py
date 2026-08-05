from dataclasses import FrozenInstanceError, replace
from datetime import timedelta

import pytest

from collector.document_admission import (
    DocumentAdmissionValidationError,
    Phase3BPolicyBundle,
    RetentionDisposition,
    phase3b_policy_bundle,
    synthetic_consumer_policy,
    synthetic_digest_policy,
    synthetic_inspection_policy,
    synthetic_resource_limit_policy,
    synthetic_retention_policy,
)

from .synthetic_fixtures import NOW, build_envelope, build_policies


def test_exact_policy_profiles_construct_and_are_immutable():
    profiles = (
        synthetic_digest_policy(),
        synthetic_consumer_policy(
            effective_at=NOW,
            expires_at=NOW + timedelta(days=1),
        ),
        synthetic_retention_policy(),
        synthetic_resource_limit_policy(),
        synthetic_inspection_policy(),
    )
    for profile in profiles:
        with pytest.raises(FrozenInstanceError):
            profile.policy_version = "2"


def test_admission_policies_match_exact_envelope_identities():
    policies = build_policies()
    policies.validate_envelope(build_envelope())

    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_envelope_policy_identity",
    ):
        policies.validate_envelope(
            build_envelope(resource_policy_version="2")
        )


def test_consumer_policy_requires_expiry_after_effect():
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_expires_at",
    ):
        synthetic_consumer_policy(
            effective_at=NOW,
            expires_at=NOW,
        )


@pytest.mark.parametrize(
    "flag",
    [
        "runtime_access_allowed",
        "api_access_allowed",
        "registry_access_allowed",
        "memory_access_allowed",
        "retrieval_access_allowed",
        "model_access_allowed",
        "interface_access_allowed",
        "real_information_access_allowed",
    ],
)
def test_consumer_policy_cannot_enable_access(flag):
    policy = synthetic_consumer_policy(
        effective_at=NOW,
        expires_at=NOW + timedelta(days=1),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match=f"invalid_{flag}",
    ):
        replace(policy, **{flag: True})


def test_phase3b_policy_bundle_is_pdf_only_and_frozen() -> None:
    policy = phase3b_policy_bundle()
    assert policy.allowed_media_type == "application/pdf"
    assert policy.max_pdf_bytes == 20 * 1024 * 1024
    with pytest.raises(FrozenInstanceError):
        policy.allowed_media_type = "text/plain"


def test_phase3b_policy_bundle_rejects_non_pdf_configuration() -> None:
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_allowed_media_type",
    ):
        Phase3BPolicyBundle(
            policy_id="phase3b-board-roster-pilot-v1",
            policy_version="1",
            allowed_media_type="image/png",
            max_pdf_bytes=1024,
            retention_days=30,
            audit_retention_days=365,
            backup_retention_days=30,
            allowed_review_decisions=(),
        )


def test_retention_policy_has_exact_dispositions():
    policy = synthetic_retention_policy()
    assert (
        policy.accepted_disposition is RetentionDisposition.DELETE
    )
    assert (
        policy.held_disposition
        is RetentionDisposition.RETAIN_TEMPORARILY
    )
    assert policy.cleanup_required is True


def test_retention_policy_cannot_create_implicit_hold():
    policy = synthetic_retention_policy()
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_rejected_disposition",
    ):
        replace(
            policy,
            rejected_disposition=RetentionDisposition.LEGAL_HOLD,
        )


def test_resource_policy_uses_exact_small_limits():
    policy = synthetic_resource_limit_policy()
    assert policy.max_input_bytes == 65_536
    assert policy.max_docx_archive_entries == 128
    assert policy.max_pdf_embedded_objects == 0

    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_max_input_bytes",
    ):
        replace(policy, max_input_bytes=65_537)


@pytest.mark.parametrize(
    "flag",
    [
        "execution_allowed",
        "network_allowed",
        "external_fetch_allowed",
        "macro_allowed",
        "embedded_payload_allowed",
        "ocr_allowed",
    ],
)
def test_resource_policy_cannot_enable_prohibited_capability(flag):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match=f"invalid_{flag}",
    ):
        replace(
            synthetic_resource_limit_policy(),
            **{flag: True},
        )


def test_inspection_policy_names_interface_isolation_only():
    policy = synthetic_inspection_policy()
    assert policy.isolation_policy_id == "synthetic-interface-isolation"
    assert policy.inspector_id == "synthetic-scripted-inspector"
