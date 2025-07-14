import logging
import sys
from pathlib import Path
from typing import Optional

import structlog
from structlog.stdlib import LoggerFactory


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = True,
    console_output: bool = True,
) -> structlog.BoundLogger:
    """
    Configura o sistema de logging estruturado.

    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log (opcional)
        json_format: Se deve usar formato JSON
        console_output: Se deve exibir logs no console

    Returns:
        Logger configurado
    """

    # Configurar structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
            if json_format
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configurar logging padrão
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Configurar handlers
    handlers = []

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        handlers.append(console_handler)

    if log_file:
        # Criar diretório de logs se não existir
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        handlers.append(file_handler)

    # Configurar logger root
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    for handler in handlers:
        root_logger.addHandler(handler)

    return structlog.get_logger()


def get_logger(name: str = "boleto_parser") -> structlog.BoundLogger:
    """
    Obtém um logger configurado.

    Args:
        name: Nome do logger

    Returns:
        Logger configurado
    """
    return structlog.get_logger(name)


# Configuração padrão
def setup_default_logging():
    """Configura logging padrão para desenvolvimento"""
    return setup_logging(
        log_level="INFO",
        log_file="logs/boleto_parser.log",
        json_format=False,  # Console formatado para desenvolvimento
        console_output=True,
    )


def setup_production_logging():
    """Configura logging para produção"""
    return setup_logging(
        log_level="INFO",
        log_file="logs/boleto_parser.json",
        json_format=True,  # JSON para produção
        console_output=False,
    )


# Logger padrão
logger = get_logger()
