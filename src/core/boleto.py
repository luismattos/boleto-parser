#!/usr/bin/env python3
"""
Classe inicial para Boleto Bancário
Estrutura básica com campos obrigatórios e opcionais conforme Febraban
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
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


@dataclass
class BoletoBancario:
    """
    Classe inicial para representar um boleto bancário
    conforme especificações da Febraban
    """
    
    # === CAMPOS OBRIGATÓRIOS ===
    
    # Código do Banco (3 dígitos)
    codigo_banco: str
    
    # Linha Digitável (47 dígitos)
    linha_digitavel: str
    
    # Código de Barras
    codigo_barras: str
    
    # Nome do Cedente
    nome_cedente: str
    
    # CNPJ/CPF do Cedente
    cnpj_cpf_cedente: str
    
    # Nome do Pagador
    nome_pagador: str
    
    # CNPJ/CPF do Pagador
    cnpj_cpf_pagador: str
    
    # Data de Vencimento
    data_vencimento: datetime
    
    # Valor do Documento
    valor_documento: float
    
    # Nosso Número
    nosso_numero: str
    
    # Carteira
    carteira: str
    
    # Data de Emissão
    data_emissao: datetime
    
    # Espécie do Documento
    especie_documento: TipoDocumento = TipoDocumento.DUPLICATA_MERCANTIL
    
    # Aceite
    aceite: TipoAceite = TipoAceite.NAO
    
    # Agência/Código do Cedente
    agencia_cedente: Optional[str] = None
    
    # Conta do Cedente
    conta_cedente: Optional[str] = None
    
    # === CAMPOS OPCIONAIS ===
    
    # Instruções
    instrucoes: List[str] = field(default_factory=list)
    
    # Descontos
    desconto_valor: Optional[float] = None
    desconto_data: Optional[datetime] = None
    desconto_percentual: Optional[float] = None
    
    # Juros e multas
    juros_percentual: Optional[float] = None
    multa_percentual: Optional[float] = None
    multa_valor: Optional[float] = None
    
    # Informações adicionais
    numero_documento: Optional[str] = None
    sacador_avalista: Optional[str] = None
    informacoes_adicionais: List[str] = field(default_factory=list)
    
    # Protesto
    protesto_dias: Optional[int] = None
    protesto_instrucao: Optional[str] = None
    
    # Uso do banco
    uso_banco: Optional[str] = None
    
    # Local de pagamento
    local_pagamento: str = "PAGÁVEL EM QUALQUER BANCO ATÉ O VENCIMENTO"
    
    # Endereços
    endereco_cedente: Optional[str] = None
    endereco_pagador: Optional[str] = None
    
    # Código do beneficiário
    codigo_beneficiario: Optional[str] = None
    
    # Moeda
    moeda: str = "9"  # Real brasileiro
    
    # === VALIDAÇÕES ===
    
    def validar_campos_obrigatorios(self) -> bool:
        """Valida se todos os campos obrigatórios estão preenchidos"""
        return (
            bool(self.codigo_banco) and
            bool(self.linha_digitavel) and
            bool(self.codigo_barras) and
            bool(self.nome_cedente) and
            bool(self.cnpj_cpf_cedente) and
            bool(self.nome_pagador) and
            bool(self.cnpj_cpf_pagador) and
            bool(self.nosso_numero) and
            bool(self.carteira) and
            self.valor_documento > 0
        )
    
    def __str__(self) -> str:
        """Representação string do boleto"""
        return (
            f"BoletoBancario("
            f"banco={self.codigo_banco}, "
            f"cedente={self.nome_cedente}, "
            f"valor=R${self.valor_documento:.2f}, "
            f"vencimento={self.data_vencimento.strftime('%d/%m/%Y')}"
            f")"
        ) 