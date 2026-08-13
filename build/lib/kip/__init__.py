"""Knowledge Ingestion Pipeline — reference implementation of specification v3.0.

Spec: docs/SPECIFICATION.md. Research backing: research/.
"""

from .artifacts import RunContext
from .config import Config, default_config

__version__ = "0.1.0"
__spec_version__ = "3.0.0"

__all__ = ["RunContext", "Config", "default_config", "__version__", "__spec_version__"]
