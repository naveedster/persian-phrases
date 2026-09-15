#!/usr/bin/env python3
"""Regenerate the bundled Daily Phrases catalog.

Kept as a stable entry point from earlier Persian-only versions. The
multilingual generator lives in ``generate_catalog.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_catalog import main

if __name__ == "__main__":
    main()
