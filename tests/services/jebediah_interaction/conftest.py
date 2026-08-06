from __future__ import annotations

from pathlib import Path
import sys


SERVICE_ROOT = (
    Path(__file__).resolve().parents[3] / "services" / "jebediah-interaction"
)
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))
