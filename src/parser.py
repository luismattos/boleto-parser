"""
Módulo de parsing de boletos bancários.

Este módulo fornece acesso às classes principais para parsing de boletos.
Para melhor organização, as implementações foram movidas para submodules.
"""

from .decoder import BoletoDecoder

# Importar classes principais do módulo parser
from .parser import BoletoParser

# Manter compatibilidade com imports existentes
__all__ = ["BoletoParser", "BoletoDecoder"]
