from fastapi import APIRouter

from ..parser import BoletoDecoder
from .schemas import DecodeResponse

router = APIRouter()
decoder = BoletoDecoder()


@router.post("/decode", response_model=DecodeResponse)
async def decode_digitavel(digitavel: str):
    """
    Decodifica um código digitável de boleto bancário.
    """
    try:
        dados = decoder.decodificar_digitavel(digitavel)
        return DecodeResponse(success=True, data=dados)
    except Exception as e:
        return DecodeResponse(success=False, error=str(e))
