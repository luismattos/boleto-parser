from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class DadosBeneficiario(BaseModel):
    """Dados do beneficiário do boleto"""

    nome: str
    cnpj: str
    agencia: str
    codigo_beneficiario: str
    nosso_numero: str


class DadosPagador(BaseModel):
    """Dados do pagador do boleto"""

    nome: str
    cpf_cnpj: str
    endereco: str
    cep: str


class DadosAluno(BaseModel):
    """Dados do aluno (para boletos educacionais)"""

    nome: str
    matricula: str
    curso: str
    turno: str
    codigo: str


class Valores(BaseModel):
    """Valores do boleto"""

    valor_documento: float
    valor_cobrado: float
    total_debitos: Optional[float] = None


class InformacoesBancarias(BaseModel):
    """Informações bancárias do boleto"""

    banco: str
    codigo_barras: str
    carteira: str
    especie: str
    aceite: str


class Instrucoes(BaseModel):
    """Instruções de pagamento"""

    local_pagamento: str
    multa_vencimento: Optional[str] = None
    juros_dia_atraso: Optional[str] = None
    restricoes: Optional[str] = None


class EnderecoInstituicao(BaseModel):
    """Endereço da instituição"""

    endereco: str
    cep: str


class BoletoData(BaseModel):
    """Estrutura completa dos dados do boleto"""

    # Informações gerais
    cnpj_instituicao: str
    numero_boleto: str
    vencimento: str
    data_documento: str

    # Dados estruturados
    beneficiario: DadosBeneficiario
    pagador: DadosPagador
    aluno: Optional[DadosAluno] = None
    valores: Valores
    informacoes_bancarias: InformacoesBancarias
    instrucoes: Instrucoes
    endereco_instituicao: EnderecoInstituicao

    # Metadados
    tipo_boleto: str = Field(
        default="educacional", description="Tipo do boleto identificado"
    )
    texto_extraido: str = Field(description="Texto bruto extraído do PDF")
    
    # Dados extras e opcionais
    dados_extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dados adicionais específicos do boleto que não se encaixam nos campos padrão"
    )
