from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..parser import BoletoParser
from .schemas import ParseResponse

router = APIRouter()
parser = BoletoParser()


@router.post("/parse", response_model=ParseResponse)
async def parse_boleto(file: UploadFile = File(...)):
    """
    Parse um arquivo PDF de boleto bancário e retorna dados estruturados.
    """
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        try:
            dados = parser.parse(str(temp_file))
            dados_dict = dados.model_dump()
            return ParseResponse(
                success=True, data=dados_dict, tipo_boleto=dados.tipo_boleto
            )
        finally:
            if temp_file.exists():
                temp_file.unlink()
    except Exception as e:
        return ParseResponse(success=False, error=str(e))
