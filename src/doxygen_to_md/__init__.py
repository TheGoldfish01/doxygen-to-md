"""doxygen_to_md

Public package interface: keep `__init__` lightweight and import the
implementation from `convert.py` so testing and CLI code import `convert`
from the package root.
"""

from __future__ import annotations

__version__ = "0.0.0"

from .convert import convert

__all__ = ["convert"]
