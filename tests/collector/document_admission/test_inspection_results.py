from dataclasses import FrozenInstanceError, replace

import pytest

from collector.document_admission import (
    ConsumerEligibilityOutcome,
    DocumentAdmissionValidationError,
    ExtractionQuality,
    TransformationState,
    synthetic_inspection_policy,
)

from .synthetic_fixtures import (
    AMBIGUOUS,
    build_admission_context,
    build_envelope,
    build_inspection_context,
    build_policies,
    build_system,
    submit_valid,
)


def inspect_with_mode(mode, **system_options):
    system = build_system(inspector_mode=mode, **system_options)
    admission = submit_valid(system)
    result = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    return system, result


def test_complete_eligible_inspection_becomes_consumer_ready():
    _, attempt = inspect_with_mode("complete")
    assert attempt.state is TransformationState.READY
    assert attempt.inspection_result.extraction_quality is (
        ExtractionQuality.COMPLETE
    )
    assert attempt.consumer_eligibility_decision.outcome is (
        ConsumerEligibilityOutcome.ELIGIBLE
    )
    assert not hasattr(attempt, "runtime_eligible")


@pytest.mark.parametrize(
    ("mode", "reason_code"),
    [
        ("partial", "partial_output"),
        ("none", "synthetic_no_output"),
        ("limit", "resource_limit_reached"),
        ("crash", "synthetic_parser_crash"),
        ("timeout", "synthetic_parser_timeout"),
    ],
)
def test_incomplete_or_failed_inspection_never_becomes_ready(
    mode,
    reason_code,
):
    _, attempt = inspect_with_mode(mode)
    assert attempt.state is TransformationState.PROCESSING_FAILED
    assert attempt.disposition_reason_code == reason_code
    assert not hasattr(attempt, "runtime_eligible")


@pytest.mark.parametrize(
    "outcome",
    [
        ConsumerEligibilityOutcome.INELIGIBLE,
        ConsumerEligibilityOutcome.UNAVAILABLE,
    ],
)
def test_noneligible_consumer_decision_prevents_ready(outcome):
    _, attempt = inspect_with_mode(
        "complete",
        eligibility_outcome=outcome,
    )
    assert attempt.state is TransformationState.PROCESSING_FAILED
    assert attempt.consumer_eligibility_decision.outcome is outcome


def test_unavailable_eligibility_evaluator_is_explicit_failure():
    _, attempt = inspect_with_mode(
        "complete",
        eligibility_unavailable=True,
    )
    assert attempt.state is TransformationState.PROCESSING_FAILED
    assert (
        attempt.disposition_reason_code
        == "synthetic_eligibility_unavailable"
    )


def test_malformed_inspector_result_fails_closed():
    system = build_system(inspector_mode="malformed")
    admission = submit_valid(system)
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_inspection_result",
    ):
        system.orchestrator.inspect(
            admission,
            synthetic_inspection_policy(),
            build_policies().consumer,
            build_inspection_context(),
        )


def test_inspection_result_is_immutable():
    _, attempt = inspect_with_mode("complete")
    with pytest.raises(FrozenInstanceError):
        attempt.inspection_result.failure_kind = "changed"


def test_output_identity_must_match_input_identity():
    _, attempt = inspect_with_mode("complete")
    result = attempt.inspection_result
    changed_output = replace(
        result.output_identity,
        input_content_identity=replace(
            result.input_content_identity,
            digest_hex="0" * 64,
        ),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_output_identity",
    ):
        replace(result, output_identity=changed_output)


def test_inspection_requires_accepted_admission():
    system = build_system()
    held = system.orchestrator.submit(
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="inspection_requires_accepted_admission",
    ):
        system.orchestrator.inspect(
            held,
            synthetic_inspection_policy(),
            build_policies().consumer,
            build_inspection_context(),
        )
