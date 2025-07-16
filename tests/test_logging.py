#!/usr/bin/env python3
"""
Teste do sistema de logging
"""

from src.utils.logger import get_logger


def test_logger_basico():
    """Testa funcionalidade básica do logger"""
    logger = get_logger("test_logger")

    # Testar diferentes níveis de log
    logger.debug("Mensagem de debug")
    logger.info("Mensagem de info")
    logger.warning("Mensagem de warning")
    logger.error("Mensagem de error")

    # Verificar que o logger foi criado corretamente
    assert logger.name == "test_logger"
    print("✅ Logger básico funcionando corretamente")


def test_logger_estruturado():
    """Testa logging estruturado com campos adicionais"""
    logger = get_logger("test_estruturado")

    # Testar logging com campos estruturados
    logger.info(
        "Processamento iniciado", arquivo="teste.pdf", tamanho=1024, status="iniciado"
    )

    logger.info(
        "Processamento concluído",
        arquivo="teste.pdf",
        resultado="sucesso",
        tempo_ms=150,
    )

    print("✅ Logger estruturado funcionando corretamente")


if __name__ == "__main__":
    test_logger_basico()
    test_logger_estruturado()
    print("✅ Todos os testes de logging passaram!")
