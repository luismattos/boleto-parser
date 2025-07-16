"""
Módulo de parsing de boletos bancários.

Este módulo contém as classes e utilitários para extrair e processar
informações de boletos bancários a partir de arquivos PDF.
"""

from .decoder import BoletoDecoder
from .extractors import (
    AlunoExtractor,
    BeneficiarioExtractor,
    BoletoDataExtractor,
    DadosExtrasExtractor,
    EnderecoInstituicaoExtractor,
    InformacoesBancariasExtractor,
    InstrucoesExtractor,
    PagadorExtractor,
    ValoresExtractor,
)
from .parser import BoletoParser

__all__ = [
    "BoletoDecoder",
    "BoletoParser",
    "BoletoDataExtractor",
    "BeneficiarioExtractor",
    "PagadorExtractor",
    "AlunoExtractor",
    "ValoresExtractor",
    "InformacoesBancariasExtractor",
    "InstrucoesExtractor",
    "EnderecoInstituicaoExtractor",
    "DadosExtrasExtractor",
]
