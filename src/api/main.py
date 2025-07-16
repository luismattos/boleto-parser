from fastapi import FastAPI

from .routes_decode import router as decode_router
from .routes_extract_text import router as extract_text_router
from .routes_health import router as health_router
from .routes_parse import router as parse_router
from .routes_validate import router as validate_router

app = FastAPI(
    title="Boleto Parser API",
    description="API para extração e interpretação de dados de boletos bancários PDF",
    version="1.0.0",
)

app.include_router(parse_router)
app.include_router(decode_router)
app.include_router(validate_router)
app.include_router(extract_text_router)
app.include_router(health_router)
