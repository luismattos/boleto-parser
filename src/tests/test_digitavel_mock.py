#!/usr/bin/env python3
"""
Teste com Mock do módulo digitavel
Demonstra como usar mocks para testar comportamentos isolados
"""

import regex

from ..core.digitavel import Digitavel
from ..utils.logger import get_logger


class TestDigitavelMock:
    """Testes com mock para a classe Digitavel"""

    def setup_method(self):
        """Setup para cada teste"""
        self.logger = get_logger("test_digitavel_mock")
        # Criar uma instância com um digitável válido
        self.digitavel_valido = "03399.12345 67890.123456 78901.234567 1 12340000012345"
        self.digitavel = Digitavel(self.digitavel_valido)

    def gerar_digitavel_valido(self, banco="033", valor=150.00, vencimento_dias=30):
        """
        Gera um código digitável válido usando o método da classe Digitavel
        """
        return Digitavel.gerar_digitavel_valido(banco, valor, vencimento_dias)

    def extrair_digitavel(self, texto):
        """Extrai código digitável do texto usando regex"""
        padroes = [
            # Formato sem formatação (47 dígitos)
            r"(\d{47})",
            # Formato com formatação (pontos e espaços)
            r"(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{14})",
            r"(\d{5}\s+\d{5}\s+\d{6}\s+\d{5}\s+\d{6}\s+\d\s+\d{14})",
        ]

        for padrao in padroes:
            match = regex.search(padrao, texto)
            if match:
                return match.group(1)
        return None

    def test_gerar_digitavel_valido(self):
        """Testa geração de código digitável válido"""
        digitavel = self.gerar_digitavel_valido(
            banco="033", valor=150.00, vencimento_dias=30
        )

        # Verificar estrutura básica (apenas dígitos)
        assert len(digitavel) == 47
        assert digitavel.isdigit()

        self.logger.info(f"✅ Código digitável gerado: {digitavel}")

    def test_parse_digitavel_mock_sucesso(self):
        """Testa parsing de código digitável com sucesso"""
        # Gerar código digitável válido
        digitavel_valido = self.gerar_digitavel_valido(
            banco="033", valor=150.00, vencimento_dias=30
        )

        # Mock do texto extraído contendo o digitável
        texto_mock = f"""
        Boleto Bancário
        Beneficiário: EMPRESA EXEMPLO LTDA
        Pagador: JOÃO DA SILVA
        
        Linha Digitável: {digitavel_valido}
        
        Valor: R$ 150,00
        Vencimento: 15/08/2025
        """

        # Testar extração do digitável
        resultado = self.extrair_digitavel(texto_mock)

        assert resultado is not None
        assert resultado == digitavel_valido

        self.logger.info(f"✅ Digitável extraído com sucesso: {resultado}")

    def test_parse_digitavel_mock_falha(self):
        """Testa parsing quando não há código digitável"""
        # Mock do texto sem digitável
        texto_mock = """
        Boleto Bancário
        Beneficiário: EMPRESA EXEMPLO LTDA
        Pagador: JOÃO DA SILVA
        
        Valor: R$ 150,00
        Vencimento: 15/08/2025
        """

        # Testar extração (deve retornar None)
        resultado = self.extrair_digitavel(texto_mock)

        assert resultado is None

        self.logger.info("✅ Comportamento correto quando não há digitável")

    def test_validar_digitavel_mock(self):
        """Testa validação de código digitável"""
        # Gerar código digitável válido
        digitavel_valido = self.gerar_digitavel_valido(
            banco="033", valor=150.00, vencimento_dias=30
        )

        # Criar instância da classe Digitavel
        digitavel_obj = Digitavel(digitavel_valido)

        # Testar validação
        assert digitavel_obj.validar() is True

        self.logger.info(f"✅ Validação bem-sucedida para: {digitavel_valido}")

    def test_decodificar_digitavel_mock(self):
        """Testa decodificação completa do código digitável"""
        # Gerar código digitável válido
        digitavel_valido = self.gerar_digitavel_valido(
            banco="033", valor=150.00, vencimento_dias=30
        )

        # Criar instância da classe Digitavel
        digitavel_obj = Digitavel(digitavel_valido)

        # Testar propriedades
        assert digitavel_obj.banco == "033"
        assert digitavel_obj.valor_documento == 150.00
        assert digitavel_obj.data_vencimento is not None
        assert digitavel_obj.codigo_barras is not None

        self.logger.info("✅ Decodificação bem-sucedida:")
        self.logger.info(f"   Banco: {digitavel_obj.banco}")
        self.logger.info(f"   Valor: R$ {digitavel_obj.valor_documento:.2f}")
        self.logger.info(f"   Vencimento: {digitavel_obj.data_vencimento}")
        self.logger.info(f"   Código de Barras: {digitavel_obj.codigo_barras}")

    def test_diferentes_bancos(self):
        """Testa geração de digitáveis para diferentes bancos"""
        bancos = ["001", "033", "104", "237", "341"]

        for banco in bancos:
            digitavel = self.gerar_digitavel_valido(
                banco=banco, valor=100.00, vencimento_dias=15
            )
            digitavel_obj = Digitavel(digitavel)

            assert digitavel_obj.banco == banco
            print(f"✅ Banco {banco}: {digitavel_obj.banco}")

    def test_diferentes_valores(self):
        """Testa geração de digitáveis com diferentes valores"""
        valores = [10.00, 50.00, 100.00, 500.00, 1000.00]

        for valor in valores:
            digitavel = self.gerar_digitavel_valido(valor=valor, vencimento_dias=30)
            digitavel_obj = Digitavel(digitavel)

            assert abs(digitavel_obj.valor_documento - valor) < 0.01
            print(f"✅ Valor R$ {valor:.2f}: {digitavel_obj.valor_documento:.2f}")

    def test_diferentes_vencimentos(self):
        """Testa geração de digitáveis com diferentes vencimentos"""
        vencimentos = [7, 15, 30, 60, 90]

        for dias in vencimentos:
            digitavel = self.gerar_digitavel_valido(valor=100.00, vencimento_dias=dias)
            digitavel_obj = Digitavel(digitavel)

            print(f"✅ Vencimento em {dias} dias: {digitavel_obj.data_vencimento}")


def test_integracao_completa():
    """Teste de integração completa com mock"""
    logger = get_logger("test_digitavel_mock_integracao")
    logger.info("🧪 TESTE DE INTEGRAÇÃO COMPLETA")
    logger.info("=" * 50)

    # Gerar código digitável válido
    digitavel_valido = Digitavel.gerar_digitavel_valido(
        banco="033", valor=250.00, vencimento_dias=45
    )
    logger.info(f"📝 Código digitável gerado: {digitavel_valido}")

    # Simular texto extraído de PDF
    texto_simulado = f"""
    BOLETO BANCÁRIO
    ================

    Beneficiário: INSTITUIÇÃO EDUCACIONAL EXEMPLO LTDA
    CNPJ: 12.345.678/0001-90

    Pagador: JOÃO DA SILVA SANTOS
    CPF: 123.456.789-00

    Linha Digitável: {digitavel_valido}

    Valor: R$ 250,00
    Vencimento: 15/08/2025

    Instruções: Pagável em qualquer banco até o vencimento
    """

    # Testar extração
    padrao = r"(\d{47})"  # Aceita 47 dígitos sem formatação
    match = regex.search(padrao, texto_simulado)
    digitavel_extraido = match.group(1) if match else None

    assert digitavel_extraido == digitavel_valido
    logger.info(f"✅ Extração correta do digitável: {digitavel_extraido}")

    # Testar validação
    digitavel_obj = Digitavel(digitavel_extraido)
    assert digitavel_obj.validar() is True
    logger.info("✅ Validação do digitável bem-sucedida")

    # Testar decodificação
    assert digitavel_obj.valor_documento == 250.00
    logger.info("✅ Decodificação do valor bem-sucedida")

    logger.info(f"   Banco: {digitavel_obj.banco}")
    logger.info(f"   Valor: R$ {digitavel_obj.valor_documento:.2f}")
    logger.info(f"   Vencimento: {digitavel_obj.data_vencimento}")
    logger.info(f"   Código de Barras: {digitavel_obj.codigo_barras}")
    logger.info("✅ Todos os testes de integração passaram!")


if __name__ == "__main__":
    # Executar testes
    test_integracao_completa()
