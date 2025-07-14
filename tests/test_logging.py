from pathlib import Path

import pytest

from src.logger import get_logger, setup_logging


def test_logging_setup():
    """Testa se o sistema de logging pode ser configurado"""
    logger = setup_logging(
        log_level="DEBUG",
        log_file="logs/test.log",
        json_format=False,
        console_output=True,
    )

    assert logger is not None

    # Testa se consegue fazer log
    logger.info("Teste de log", teste=True)
    logger.error("Teste de erro", erro="teste")

    # Verifica se arquivo foi criado
    log_file = Path("logs/test.log")
    assert log_file.exists()

    # Limpa arquivo de teste
    log_file.unlink()


def test_logger_get():
    """Testa se consegue obter logger"""
    logger = get_logger("test_logger")
    assert logger is not None

    # Testa log com contexto
    logger.info("Teste com contexto", campo="valor")


def test_logging_levels():
    """Testa diferentes níveis de log"""
    logger = get_logger("test_levels")

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    # Todos devem executar sem erro
    assert True
