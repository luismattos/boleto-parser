"""
Enumerações do sistema de boletos bancários.

Este módulo contém todas as enumerações utilizadas no sistema,
seguindo as especificações da Febraban.
"""

from enum import Enum


class TipoDocumento(Enum):
    """Tipos de documento conforme Febraban"""

    DUPLICATA_MERCANTIL = "DM"
    DUPLICATA_SERVICO = "DS"
    DUPLICATA_RURAL = "DR"
    LETRA_CAMBIO = "LC"
    NOTA_PROMISSORIA = "NP"
    RECIBO = "RC"
    APOLICE_SEGURO = "AP"
    MENSALIDADE_ESCOLAR = "ME"
    PARCELA_CONSORCIO = "PC"
    OUTROS = "OU"


class TipoAceite(Enum):
    """Tipos de aceite"""

    SIM = "S"
    NAO = "N"


class TipoMoeda(Enum):
    """Tipos de moeda"""

    REAL = "9"
    OUTRAS = "0"


class TipoCarteira(Enum):
    """Tipos de carteira bancária"""

    COBRANCA_SIMPLES = "1"
    COBRANCA_CAUCIONADA = "2"
    COBRANCA_DESCONTADA = "3"
    VENDOR = "4"
    COBRANCA_VENDOR = "5"
    COBRANCA_CAUCIONADA_ELETRONICA = "6"
    COBRANCA_SIMPLES_ELETRONICA = "7"
    COBRANCA_CAUCIONADA_ELETRONICA_EMISSAO_BANCO = "8"
    COBRANCA_SIMPLES_ELETRONICA_EMISSAO_BANCO = "9"
