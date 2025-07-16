from fastapi import APIRouter

router = APIRouter()


@router.get("/")
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


@router.get("/health")
async def health_check():
    """Health check da API"""
    return {"status": "healthy", "service": "boleto-parser-api"}
