"""Metadata providers exposed through the v3 source-adapter contract."""

from .crossref import CrossrefProvider
from .openalex import OpenAlexProvider

__all__ = ["CrossrefProvider", "OpenAlexProvider"]
