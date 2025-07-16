from typing import Optional

from pydantic import BaseModel


class Valores(BaseModel):
    """Valores do boleto"""

    valor_documento: float
    valor_cobrado: float
    total_debitos: Optional[float] = None
