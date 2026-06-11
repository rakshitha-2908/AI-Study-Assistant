"""Pytest configuration file for proper module imports."""

import sys
from pathlib import Path

# Add src directory to Python path so tests can import from agent module
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
