from pydantic import BaseModel


class DadosBeneficiario(BaseModel):
    """Dados do beneficiário do boleto"""

    nome: str
    cnpj: str
    agencia: str
    codigo_beneficiario: str
    nosso_numero: str
