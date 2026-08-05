from dataclasses import fields, replace

import pytest

from collector.document_admission import (
    DocumentAdmissionValidationError,
    TransformationState,
    synthetic_inspection_policy,
)

from .synthetic_fixtures import (
    NOW,
    build_inspection_context,
    build_policies,
    build_resource_observation,
    build_system,
    synthetic_resource_limit_policy,
    submit_valid,
)


RESOURCE_LIMIT_NAMES = tuple(
    field.name
    for field in fields(synthetic_resource_limit_policy())
    if field.name.startswith("max_")
)


def test_resource_observation_is_deterministic():
    assert build_resource_observation() == build_resource_observation()
    assert hash(build_resource_observation()) == hash(
        build_resource_observation()
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "observed_input_bytes",
        "observed_cpu_milliseconds",
        "observed_pdf_pages",
        "observed_docx_archive_entries",
    ],
)
def test_resource_observation_rejects_negative_values(field_name):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match=f"invalid_{field_name}",
    ):
        build_resource_observation(**{field_name: -1})


def test_exceeded_limit_names_must_be_known_resource_fields():
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_exceeded_limit_names",
    ):
        build_resource_observation(
            exceeded_limit_names=("unknown_limit",)
        )


def test_exceeded_resource_limit_prevents_ready_state():
    system = build_system(inspector_mode="limit")
    admission = submit_valid(system)
    attempt = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    assert attempt.state is TransformationState.PROCESSING_FAILED
    assert attempt.disposition_reason_code == "resource_limit_reached"
    assert attempt.inspection_result.reached_limit_names == (
        "max_cpu_milliseconds",
    )


@pytest.mark.parametrize("limit_name", RESOURCE_LIMIT_NAMES)
def test_every_resource_limit_above_threshold_fails(limit_name):
    system = build_system(inspector_mode=f"limit:{limit_name}")
    admission = submit_valid(system)
    attempt = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    assert attempt.state is TransformationState.PROCESSING_FAILED
    assert attempt.inspection_result.reached_limit_names == (
        limit_name,
    )


@pytest.mark.parametrize("limit_name", RESOURCE_LIMIT_NAMES)
def test_every_resource_limit_at_and_below_threshold_is_representable(
    limit_name,
):
    maximum = getattr(synthetic_resource_limit_policy(), limit_name)
    observed_name = limit_name.replace("max_", "observed_", 1)
    at_limit = build_resource_observation(
        **{observed_name: maximum}
    )
    assert getattr(at_limit, observed_name) == maximum
    assert at_limit.exceeded_limit_names == ()
    if maximum > 0:
        below_limit = build_resource_observation(
            **{observed_name: maximum - 1}
        )
        assert getattr(below_limit, observed_name) == maximum - 1


def test_resource_observation_requires_aware_timestamp():
    observation = build_resource_observation()
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_observed_at",
    ):
        replace(observation, observed_at=NOW.replace(tzinfo=None))
