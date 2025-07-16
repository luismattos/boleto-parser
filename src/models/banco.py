from pydantic import BaseModel


class InformacoesBancarias(BaseModel):
    """Informações bancárias do boleto"""

    banco: str
    codigo_barras: str
    carteira: str
    especie: str
    aceite: str
