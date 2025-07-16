# Utils Module - Utilitários do sistema

from .dv import modulo_10, modulo_11
from .logger import (
    get_logger,
    logger,
    setup_default_logging,
    setup_logging,
    setup_production_logging,
)

__all__ = [
    "get_logger",
    "setup_logging",
    "setup_default_logging",
    "setup_production_logging",
    "logger",
    "modulo_10",
    "modulo_11",
]
