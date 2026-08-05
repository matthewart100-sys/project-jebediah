import pytest

from collector.document_admission import (
    AdmissionState,
    EvaluationOutcome,
)

from .synthetic_fixtures import (
    ACTIVE_CONTENT,
    AMBIGUOUS_ACTIVE_CONTENT,
    ENCRYPTED,
    PROMPT_INJECTION,
    build_admission_context,
    build_envelope,
    build_policies,
    build_system,
)


@pytest.mark.parametrize(
    ("payload", "safe_name", "media_type", "reason_code"),
    [
        (
            ENCRYPTED,
            "synthetic.pdf",
            "application/pdf",
            "encrypted_input",
        ),
        (
            ACTIVE_CONTENT,
            "synthetic.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "active_content",
        ),
    ],
)
def test_known_unsafe_indicators_are_rejected(
    payload,
    safe_name,
    media_type,
    reason_code,
):
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(
            supplied_name=safe_name,
            safe_name=safe_name,
            claimed_media_type=media_type,
        ),
        payload,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is AdmissionState.REJECTED
    assert result.security_evaluation.outcome is EvaluationOutcome.REJECT
    assert result.disposition_reason_code == reason_code


def test_unknown_active_content_is_held():
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(
            supplied_name="synthetic.pdf",
            safe_name="synthetic.pdf",
            claimed_media_type="application/pdf",
        ),
        AMBIGUOUS_ACTIVE_CONTENT,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is AdmissionState.HELD
    assert result.security_evaluation.outcome is EvaluationOutcome.HOLD


def test_prompt_injection_marker_remains_inert_evidence():
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(),
        PROMPT_INJECTION,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is AdmissionState.ACCEPTED
    assert result.security_evaluation.evidence_references == (
        "prompt_injection_inert",
    )
    assert not hasattr(result, "runtime_eligible")


def test_oversize_input_is_rejected_before_security_success():
    system = build_system()
    payload = b"S" * (build_policies().resources.max_input_bytes + 1)
    from collector.document_admission import ResourceLimitExceeded

    with pytest.raises(
        ResourceLimitExceeded,
        match="max_input_bytes_exceeded",
    ):
        system.orchestrator.submit(
            build_envelope(),
            payload,
            build_policies(),
            build_admission_context(),
        )
