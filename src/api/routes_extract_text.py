from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..parser import BoletoParser

router = APIRouter()
parser = BoletoParser()


@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Extrai texto bruto de um arquivo PDF.
    """
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        try:
            texto = parser.extrair_texto_pdf(str(temp_file))
            return {"success": True, "texto": texto, "tamanho": len(texto)}
        finally:
            if temp_file.exists():
                temp_file.unlink()
    except Exception as e:
        return {"success": False, "error": str(e)}
