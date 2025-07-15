# Core Module - Classes principais do sistema

from .boleto import BoletoBancario, TipoDocumento, TipoAceite
from .digitavel import Digitavel, CamposDigitavel

__all__ = [
    "BoletoBancario",
    "TipoDocumento", 
    "TipoAceite",
    "Digitavel",
    "CamposDigitavel"
] 