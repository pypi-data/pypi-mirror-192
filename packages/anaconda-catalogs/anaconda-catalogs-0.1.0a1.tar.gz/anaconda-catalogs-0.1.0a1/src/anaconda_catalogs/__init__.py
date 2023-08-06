"""anaconda.catalogs is a library allowing users to interface with Anaconda's Intake catalogs service."""
from typing import Optional

from intake import Catalog

from .catalog import AnacondaCatalog

__all__ = ["__version__", "open_catalog", "AnacondaCatalog"]

__version__ = "0.1.0a1"


def open_catalog(slug: str, base_uri: Optional[str] = None) -> Catalog:
    """Open an Intake catalog hosted on Anaconda Catalogs."""
    return AnacondaCatalog(slug=slug, base_uri=base_uri)
