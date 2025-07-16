from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .aluno import DadosAluno
from .banco import InformacoesBancarias
from .beneficiario import DadosBeneficiario
from .endereco import EnderecoInstituicao
from .instrucoes import Instrucoes
from .pagador import DadosPagador
from .valores import Valores


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
        description=(
            "Dados adicionais específicos do boleto que não se encaixam nos campos padrão"
        ),
    )
