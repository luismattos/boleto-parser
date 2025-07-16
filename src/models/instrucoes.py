from typing import Optional

from pydantic import BaseModel


class Instrucoes(BaseModel):
    """Instruções de pagamento"""

    local_pagamento: str
    multa_vencimento: Optional[str] = None
    juros_dia_atraso: Optional[str] = None
    restricoes: Optional[str] = None
