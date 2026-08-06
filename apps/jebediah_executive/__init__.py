"""Executive Product Shell package.

This package owns presentation, navigation, and bounded workflow interfaces for
the Bonsaai executive shell. It defaults to an operational workspace provider
that supports demonstration, development, and production modes while preserving
the existing module routes and layout.
"""

from __future__ import annotations

from .app import BriefingProvider, create_app
from .fixtures import SCENARIO_ID, SyntheticBriefingProvider
from .routes import (
    ALLOWLISTED_PRESET_IDS,
    ALLOWLISTED_STATE_IDS,
    PRODUCT_ROUTES,
)

__all__ = (
    "ALLOWLISTED_PRESET_IDS",
    "ALLOWLISTED_STATE_IDS",
    "BriefingProvider",
    "PRODUCT_ROUTES",
    "SCENARIO_ID",
    "SyntheticBriefingProvider",
    "create_app",
)
