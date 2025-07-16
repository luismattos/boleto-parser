from pydantic import BaseModel


class DadosPagador(BaseModel):
    """Dados do pagador do boleto"""

    nome: str
    cpf_cnpj: str
    endereco: str
    cep: str
