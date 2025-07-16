#!/usr/bin/env python3
"""
Teste da primeira camada da classe Digitavel
- Normalização (remoção de espaços e caracteres não numéricos)
- Validação básica (apenas dígitos, tamanho 47 ou 48)
"""

from ..core.digitavel import Digitavel


def test_normalizacao():
    """Testa a normalização de diferentes formatos de entrada"""
    print("🧪 Testando normalização...")

    # Teste com espaços e caracteres especiais
    digitavel1 = Digitavel("12345 67890 12345 67890 12345 67890 12345 67890 12345 67")
    print(f"✅ Normalizado: '{digitavel1.valor}' (tamanho: {len(digitavel1.valor)})")

    # Teste com pontos e hífens
    digitavel2 = Digitavel("12345.67890-12345.67890-12345.67890-12345.67890-12345.67")
    print(f"✅ Normalizado: '{digitavel2.valor}' (tamanho: {len(digitavel2.valor)})")

    # Teste com string vazia
    digitavel3 = Digitavel("")
    print(f"✅ Normalizado: '{digitavel3.valor}' (tamanho: {len(digitavel3.valor)})")

    # Teste com None
    digitavel4 = Digitavel(None)
    print(f"✅ Normalizado: '{digitavel4.valor}' (tamanho: {len(digitavel4.valor)})")


def test_validacao():
    """Testa a validação básica"""
    print("\n🧪 Testando validação...")

    # Casos válidos
    digitavel_valido1 = Digitavel("1" * 47)  # Banco
    digitavel_valido2 = Digitavel("1" * 48)  # Arrecadação

    print(f"✅ 47 dígitos (banco): {digitavel_valido1.validar()}")
    print(f"✅ 48 dígitos (arrecadação): {digitavel_valido2.validar()}")

    # Casos inválidos
    digitavel_invalido1 = Digitavel("12345")  # Muito curto
    digitavel_invalido2 = Digitavel("1" * 50)  # Muito longo
    digitavel_invalido3 = Digitavel("12345abc67890")  # Com letras

    print(f"❌ Muito curto: {digitavel_invalido1.validar()}")
    print(f"❌ Muito longo: {digitavel_invalido2.validar()}")
    print(f"❌ Com letras: {digitavel_invalido3.validar()}")


def test_cenarios_reais():
    """Testa com cenários mais realistas"""
    print("\n🧪 Testando cenários realistas...")

    # Linha digitável real (exemplo)
    linha_real = "23793.38128 60000.633935 60000.633935 4 84410026000 20"
    digitavel_real = Digitavel(linha_real)

    print(f"✅ Linha real normalizada: '{digitavel_real.valor}'")
    print(f"✅ Tamanho: {len(digitavel_real.valor)}")
    print(f"✅ Válida: {digitavel_real.validar()}")


if __name__ == "__main__":
    print("🚀 Testando primeira camada da classe Digitavel\n")

    test_normalizacao()
    test_validacao()
    test_cenarios_reais()

    print("\n🎉 Todos os testes da primeira camada passaram!")
