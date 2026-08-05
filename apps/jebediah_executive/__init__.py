"""Executive Product Shell (Phase 3A synthetic local preview).

This package renders one immutable, evidence-bearing executive briefing over
compiled fabricated fixtures. It owns presentation, navigation, and
deterministic synthetic demonstration behavior only.

It has no source-record, verification, derivation, approval, action,
live-information, persistence, or deployment authority, and it imports no
Collector, Knowledge Registry, Memory Service, model, retrieval, workflow, or
external-service package.

All data in this package is fabricated. It is not real organizational
information and must never be treated as live, current, verified, complete,
production, or operational.
"""

from __future__ import annotations

from .app import create_app
from .fixtures import SCENARIO_ID, SyntheticBriefingProvider
from .routes import (
    ALLOWLISTED_PRESET_IDS,
    ALLOWLISTED_STATE_IDS,
    PRODUCT_ROUTES,
)

__all__ = (
    "ALLOWLISTED_PRESET_IDS",
    "ALLOWLISTED_STATE_IDS",
    "PRODUCT_ROUTES",
    "SCENARIO_ID",
    "SyntheticBriefingProvider",
    "create_app",
)
