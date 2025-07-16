from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..parser import BoletoParser

router = APIRouter()
parser = BoletoParser()


@router.post("/validate")
async def validate_boleto(file: UploadFile = File(...)):
    """
    Valida se um arquivo PDF é um boleto válido.
    """
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        try:
            tipo_arquivo = parser.detectar_tipo_arquivo(str(temp_file))
            if "PDF" not in tipo_arquivo:
                return {
                    "valid": False,
                    "error": f"Arquivo não é um PDF válido: {tipo_arquivo}",
                }
            texto = parser.extrair_texto_pdf(str(temp_file))
            elementos_boleto = [
                "Beneficiário",
                "Pagador",
                "Vencimento",
                "Valor",
                "CNPJ",
            ]
            encontrados = [e for e in elementos_boleto if e in texto]
            is_valid = len(encontrados) >= 3
            return {
                "valid": is_valid,
                "tipo_arquivo": tipo_arquivo,
                "elementos_encontrados": encontrados,
                "total_elementos": len(encontrados),
            }
        finally:
            if temp_file.exists():
                temp_file.unlink()
    except Exception as e:
        return {"valid": False, "error": str(e)}
