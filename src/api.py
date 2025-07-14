import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .parser import BoletoParser, BoletoDecoder

app = FastAPI(
    title="Boleto Parser API",
    description="API para extração e interpretação de dados de boletos bancários PDF",
    version="1.0.0",
)

parser = BoletoParser()
decoder = BoletoDecoder()


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


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Boleto Parser API",
        "version": "1.0.0",
        "endpoints": {
            "/parse": "POST - Parse arquivo PDF de boleto",
            "/decode": "POST - Decodificar código digitável",
            "/validate": "POST - Validar se arquivo é boleto válido",
            "/extract-text": "POST - Extrair texto bruto do PDF",
        },
    }


@app.post("/parse", response_model=ParseResponse)
async def parse_boleto(file: UploadFile = File(...)):
    """
    Parse um arquivo PDF de boleto bancário e retorna dados estruturados.

    Args:
        file: Arquivo PDF do boleto

    Returns:
        JSON com dados estruturados do boleto
    """
    try:
        # Verificar tipo do arquivo
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")

        # Salvar arquivo temporário
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        try:
            # Processar boleto
            dados = parser.parse(str(temp_file))

            # Converter para dict
            dados_dict = dados.model_dump()

            return ParseResponse(
                success=True, data=dados_dict, tipo_boleto=dados.tipo_boleto
            )

        finally:
            # Limpar arquivo temporário
            if temp_file.exists():
                temp_file.unlink()

    except Exception as e:
        return ParseResponse(success=False, error=str(e))


@app.post("/decode", response_model=DecodeResponse)
async def decode_digitavel(digitavel: str):
    """
    Decodifica um código digitável de boleto bancário.

    Args:
        digitavel: Código digitável do boleto (ex: 03399.16140 70000.019182 81556.601014 4 11370000038936)

    Returns:
        JSON com dados decodificados do boleto
    """
    try:
        # Decodificar código digitável
        dados = decoder.decodificar_digitavel(digitavel)

        return DecodeResponse(success=True, data=dados)

    except Exception as e:
        return DecodeResponse(success=False, error=str(e))


@app.post("/validate")
async def validate_boleto(file: UploadFile = File(...)):
    """
    Valida se um arquivo PDF é um boleto válido.

    Args:
        file: Arquivo PDF para validar

    Returns:
        JSON com resultado da validação
    """
    try:
        # Verificar tipo do arquivo
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")

        # Salvar arquivo temporário
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        try:
            # Detectar tipo do arquivo
            tipo_arquivo = parser.detectar_tipo_arquivo(str(temp_file))

            if "PDF" not in tipo_arquivo:
                return {
                    "valid": False,
                    "error": f"Arquivo não é um PDF válido: {tipo_arquivo}",
                }

            # Extrair texto para validação
            texto = parser.extrair_texto_pdf(str(temp_file))

            # Verificar se contém elementos de boleto
            elementos_boleto = [
                "Beneficiário",
                "Pagador",
                "Vencimento",
                "Valor",
                "CNPJ",
            ]

            encontrados = []
            for elemento in elementos_boleto:
                if elemento in texto:
                    encontrados.append(elemento)

            is_valid = len(encontrados) >= 3

            return {
                "valid": is_valid,
                "tipo_arquivo": tipo_arquivo,
                "elementos_encontrados": encontrados,
                "total_elementos": len(encontrados),
            }

        finally:
            # Limpar arquivo temporário
            if temp_file.exists():
                temp_file.unlink()

    except Exception as e:
        return {"valid": False, "error": str(e)}


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Extrai texto bruto de um arquivo PDF.

    Args:
        file: Arquivo PDF

    Returns:
        JSON com texto extraído
    """
    try:
        # Verificar tipo do arquivo
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser um PDF")

        # Salvar arquivo temporário
        temp_file = Path(f"/tmp/{file.filename}")
        with open(temp_file, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        try:
            # Extrair texto
            texto = parser.extrair_texto_pdf(str(temp_file))

            return {"success": True, "texto": texto, "tamanho": len(texto)}

        finally:
            # Limpar arquivo temporário
            if temp_file.exists():
                temp_file.unlink()

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/health")
async def health_check():
    """Health check da API"""
    return {"status": "healthy", "service": "boleto-parser-api"}
