from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from apps.jebediah_executive.governed_provider import (
    GovernedRuntimeBriefingProvider,
    OperationalWorkspaceProvider,
)
from apps.jebediah_executive.models import AskState, WorkspaceKind, WorkspaceState


def _provider() -> GovernedRuntimeBriefingProvider:
    runtime_dir = Path(tempfile.mkdtemp(prefix="gov-provider-test-"))
    return GovernedRuntimeBriefingProvider(runtime_dir)


def test_governed_provider_starts_with_synthetic_defaults() -> None:
    provider = _provider()
    briefing = provider.briefing()
    assert briefing.scenario_id == "synthetic-nonprofit-demo-v1"
    assert any("governed runtime records" in item for item in briefing.limitations)


def test_governed_provider_admission_promotion_and_grounded_ask() -> None:
    provider = _provider()
    provider.admit_submission(
        payload=b"Leadership reconciled the final cash variance and approved closure.",
        source_record_id="source-record-009",
        file_name="board-update.txt",
        media_type="text/plain",
    )
    provider.promote_latest_candidate()
    provider.ask_question("What decision should leadership make next?")

    briefing = provider.briefing()
    assert any(record.kind is WorkspaceKind.DOCUMENT for record in briefing.workspace_records)
    assert any(
        record.state is WorkspaceState.ELIGIBLE for record in briefing.workspace_records
    )
    grounded = briefing.ask_response("grounded-priorities")
    assert grounded.state is AskState.GROUNDED
    assert grounded.statement is not None
    assert grounded.source_references
    assert any("answer.grounded" in activity.summary for activity in briefing.activities)


def test_governed_provider_returns_insufficient_when_no_promoted_knowledge() -> None:
    provider = _provider()
    provider.ask_question("What is the cash outlook?")
    briefing = provider.briefing()
    grounded = briefing.ask_response("grounded-priorities")
    assert grounded.state is AskState.INSUFFICIENT
    assert grounded.statement is None


def test_governed_provider_stages_image_as_needs_evidence() -> None:
    provider = _provider()
    provider.admit_submission(
        payload=b"\x89PNG\r\n\x1a\nsynthetic",
        source_record_id="source-record-100",
        file_name="scan.png",
        media_type="image/png",
    )
    briefing = provider.briefing()
    assert any(record.state is WorkspaceState.HELD for record in briefing.workspace_records)


def test_workspace_provider_defaults_to_demonstration_mode() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    briefing = provider.briefing()
    assert briefing.workspace_context.mode.value == "demonstration"
    assert briefing.workspace_context.banner_label == "Demonstration Mode"
    assert briefing.workspace_context.demo_reset_available is True


def test_workspace_provider_switches_modes_and_organizations() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    provider.select_organization("virginia-b-andes")
    provider.select_workspace("development")
    briefing = provider.briefing()
    assert briefing.workspace_context.mode.value == "development"
    assert briefing.workspace_context.profile.name == "Virginia B. Andes"

    provider.select_workspace("production")
    production = provider.briefing()
    assert production.workspace_context.mode.value == "production"
    assert production.workspace_context.banner_label == "Production Workspace"


def test_workspace_provider_blocks_live_mutation_in_demo_mode() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    with pytest.raises(RuntimeError):
        provider.admit_document("Synthetic text", "source-record-001")
