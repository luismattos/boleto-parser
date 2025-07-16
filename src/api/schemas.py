from typing import Optional

from pydantic import BaseModel


class ParseResponse(BaseModel):
    """Resposta da API de parsing"""

    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    tipo_boleto: Optional[str] = None


class DecodeResponse(BaseModel):
    """Resposta da API de decodificação"""

    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
