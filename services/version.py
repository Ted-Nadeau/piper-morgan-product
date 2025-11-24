"""
Application version management

Single source of truth: pyproject.toml
Provides __version__ for internal use and get_version_info() for API
"""

from pathlib import Path
from typing import Any, Dict

import tomli


def get_version() -> str:
    """Read version from pyproject.toml (single source of truth)"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    return pyproject["project"]["version"]


def get_version_info() -> Dict[str, Any]:
    """
    Get comprehensive version information for API responses

    Returns:
        dict: Version information including version number, environment, etc.
    """
    import os

    return {
        "version": __version__,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": "3.9+",  # From pyproject.toml requires-python
        "api_version": "v1",
    }


# Export version for import usage
__version__ = get_version()
