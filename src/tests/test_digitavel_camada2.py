#!/usr/bin/env python3
"""
Teste da segunda camada da classe Digitavel
- Validação completa dos DVs (Módulo 10 e Módulo 11)
- Correção de DVs incorretos
"""

from ..core.digitavel import Digitavel


def test_validacao_dv_completa():
    """Testa a validação completa dos DVs"""
    print("🧪 Testando validação completa dos DVs...")

    # Linha digitável real (exemplo válido)
    linha_valida = "2379338128600006339356000063393548441002600020"
    digitavel_valido = Digitavel(linha_valida)

    print(f"✅ Linha válida: {digitavel_valido.validar()}")

    # Linha digitável com DVs incorretos
    linha_invalida = "2379338128600006339356000063393548441002600021"  # DV alterado
    digitavel_invalido = Digitavel(linha_invalida)

    print(f"❌ Linha inválida: {digitavel_invalido.validar()}")


def test_correcao_dv():
    """Testa a correção de DVs incorretos"""
    print("\n🧪 Testando correção de DVs...")

    # Linha digitável com DVs incorretos
    linha_com_dv_errado = "2379338128600006339356000063393548441002600021"
    digitavel_errado = Digitavel(linha_com_dv_errado)

    print(f"📝 Linha original: {linha_com_dv_errado}")
    print(f"❌ Válida: {digitavel_errado.validar()}")

    # Corrigir DVs
    linha_corrigida = digitavel_errado.corrigir_dv()
    digitavel_corrigido = Digitavel(linha_corrigida)

    print(f"🔧 Linha corrigida: {linha_corrigida}")
    print(f"✅ Válida após correção: {digitavel_corrigido.validar()}")


def test_geracao_codigo_barras():
    """Testa a geração do código de barras"""
    print("\n🧪 Testando geração do código de barras...")

    linha_digitavel = "2379338128600006339356000063393548441002600020"
    digitavel = Digitavel(linha_digitavel)

    codigo_barras = digitavel._gerar_codigo_barras()
    print(f"📊 Código de barras gerado: {codigo_barras}")
    print(f"📏 Tamanho: {len(codigo_barras)}")


def test_calculos_modulo():
    """Testa os cálculos de Módulo 10 e Módulo 11"""
    print("\n🧪 Testando cálculos de módulo...")

    digitavel = Digitavel("1234567890")

    # Teste Módulo 10
    resultado_mod10 = digitavel._calcular_modulo_10("123456789")
    print(f"🔢 Módulo 10 para '123456789': {resultado_mod10}")

    # Teste Módulo 11
    resultado_mod11 = digitavel._calcular_modulo_11("123456789")
    print(f"🔢 Módulo 11 para '123456789': {resultado_mod11}")


def test_validacao_campos():
    """Testa a validação de campos individuais"""
    print("\n🧪 Testando validação de campos...")

    digitavel = Digitavel("2379338128600006339356000063393548441002600020")

    # Campos da linha digitável
    campo1 = "2379338128"
    campo2 = "6000063393"
    campo3 = "5600006339"

    print(f"✅ Campo 1 válido: {digitavel._validar_campo(campo1)}")
    print(f"✅ Campo 2 válido: {digitavel._validar_campo(campo2)}")
    print(f"✅ Campo 3 válido: {digitavel._validar_campo(campo3)}")


def test_digitavel_real_boleto_exemplo():
    """Testa a validação com a linha digitável real do boleto-exemplo.txt"""
    print("\n🧪 Testando linha digitável real do boleto-exemplo.txt...")
    linha_formatada = "0339916140 07000001912 81556001014 4 11370000038936"
    linha_digitavel = linha_formatada.replace(" ", "").replace(".", "")
    digitavel = Digitavel(linha_digitavel)
    print(f"📝 Linha digitável: {linha_digitavel}")
    print(f"✅ Válida: {digitavel.validar()}")


def test_digitavel_detalhado():
    """Mostra a validação detalhada dos campos/DVs da linha digitável fornecida pelo usuário"""
    print("\n🧪 Testando linha digitável detalhada fornecida pelo usuário...")
    linha_formatada = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"
    linha_digitavel = linha_formatada.replace(" ", "").replace(".", "")
    digitavel = Digitavel(linha_digitavel)
    print(f"📝 Linha digitável: {linha_digitavel}")
    print(f"✅ Válida: {digitavel.validar()}")

    # Campos
    campo1 = linha_digitavel[0:10]
    campo2 = linha_digitavel[10:20]
    campo3 = linha_digitavel[20:30]
    campo4 = linha_digitavel[30:31]
    campo5 = linha_digitavel[31:]

    print(f"\nCampos:")
    print(f"  Campo 1: {campo1} | Válido: {digitavel._validar_campo(campo1)}")
    print(f"  Campo 2: {campo2} | Válido: {digitavel._validar_campo(campo2)}")
    print(f"  Campo 3: {campo3} | Válido: {digitavel._validar_campo(campo3)}")
    print(f"  Campo 4 (DV geral): {campo4}")
    print(f"  Campo 5: {campo5}")

    # Código de barras e DV geral
    codigo_barras = digitavel._gerar_codigo_barras()
    print(f"\nCódigo de barras gerado: {codigo_barras}")
    print(f"DV geral válido: {digitavel._validar_dv_geral(codigo_barras)}")


def test_nova_estrategia():
    """Testa a nova estratégia de normalização, split e preenchimento de objeto"""
    print("\n🧪 Testando nova estratégia (normalização + split + objeto)...")
    linha_formatada = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"
    digitavel = Digitavel(linha_formatada)

    print(f"📝 Linha original: {linha_formatada}")
    print(f"🧹 Linha normalizada: {digitavel.valor}")
    print(f"✅ Válida: {digitavel.validar()}")

    if digitavel._campos:
        print(f"\nCampos extraídos:")
        print(
            f"  Bloco Campo 1: {digitavel._campos.bloco_campo1} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo1)}"
        )
        print(
            f"  Bloco Campo 2: {digitavel._campos.bloco_campo2} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo2)}"
        )
        print(
            f"  Bloco Campo 3: {digitavel._campos.bloco_campo3} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo3)}"
        )
        print(f"  DV Geral: {digitavel._campos.dv_geral}")
        print(f"  Fator/Valor: {digitavel._campos.fator_valor_e_valor}")

        print(f"\nInformações extraídas:")
        print(f"  🏦 Banco: {digitavel.banco}")
        print(f"  💰 Moeda: {digitavel._campos.moeda}")
        print(f"  📋 Campo Livre: {digitavel.campo_livre}")
        print(f"  📅 Fator Vencimento: {digitavel.fator_vencimento}")
        print(f"  💵 Valor (centavos): {digitavel.valor_centavos}")
        print(f"  💵 Valor (reais): R$ {digitavel.valor_documento:.2f}")
        print(f"  📅 Data Vencimento: {digitavel.data_vencimento}")

        # Código de barras
        codigo_barras = digitavel.codigo_barras
        print(f"  📊 Código de Barras: {codigo_barras}")
        print(
            f"  ✅ DV Geral válido: {digitavel._validar_dv_geral(codigo_barras) if codigo_barras else False}"
        )


def test_linha_digitavel_real():
    """Testa a linha digitável real do boleto-exemplo.txt"""
    print("\n🧪 Testando linha digitável real do boleto-exemplo.txt...")
    linha_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"
    digitavel = Digitavel(linha_real)

    print(f"📝 Linha original: {linha_real}")
    print(f"🧹 Linha normalizada: {digitavel.valor}")
    print(f"✅ Válida: {digitavel.validar()}")

    if digitavel._campos:
        print(f"\nCampos extraídos:")
        print(
            f"  Bloco Campo 1: {digitavel._campos.bloco_campo1} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo1)}"
        )
        print(
            f"  Bloco Campo 2: {digitavel._campos.bloco_campo2} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo2)}"
        )
        print(
            f"  Bloco Campo 3: {digitavel._campos.bloco_campo3} | Válido: {digitavel._validar_campo(digitavel._campos.bloco_campo3)}"
        )
        print(f"  DV Geral: {digitavel._campos.dv_geral}")
        print(f"  Fator/Valor: {digitavel._campos.fator_valor_e_valor}")

        print(f"\nInformações extraídas:")
        print(f"  🏦 Banco: {digitavel.banco}")
        print(f"  💰 Moeda: {digitavel._campos.moeda}")
        print(f"  📋 Campo Livre: {digitavel.campo_livre}")
        print(f"  📅 Fator Vencimento: {digitavel.fator_vencimento}")
        print(f"  💵 Valor (centavos): {digitavel.valor_centavos}")
        print(f"  💵 Valor (reais): R$ {digitavel.valor_documento:.2f}")
        print(f"  📅 Data Vencimento: {digitavel.data_vencimento}")

        # Código de barras
        codigo_barras = digitavel.codigo_barras
        print(f"  📊 Código de Barras: {codigo_barras}")
        print(
            f"  ✅ DV Geral válido: {digitavel._validar_dv_geral(codigo_barras) if codigo_barras else False}"
        )


def exibir_objeto_digitavel():
    """Exibe o objeto Digitavel completo com todos os atributos e propriedades"""
    print("\n🔍 EXIBINDO OBJETO DIGITAVEL COMPLETO")
    print("=" * 60)

    linha_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"
    digitavel = Digitavel(linha_real)

    print(f"📝 Linha Original: {linha_real}")
    print(f"🧹 Valor Normalizado: {digitavel.valor}")
    print(f"📏 Tamanho: {len(digitavel.valor)} dígitos")
    print(f"✅ Válido: {digitavel.validar()}")

    if digitavel._campos:
        print(f"\n🏗️  OBJETO CAMPOS:")
        print(f"   bloco_campo1: {digitavel._campos.bloco_campo1}")
        print(f"   bloco_campo2: {digitavel._campos.bloco_campo2}")
        print(f"   bloco_campo3: {digitavel._campos.bloco_campo3}")
        print(f"   dv_geral: {digitavel._campos.dv_geral}")
        print(f"   fator_valor_e_valor: {digitavel._campos.fator_valor_e_valor}")

        print(f"\n🔢 DÍGITOS VERIFICADORES:")
        print(f"   campo1_sem_dv: {digitavel._campos.campo1_sem_dv}")
        print(f"   dv_campo1: {digitavel._campos.dv_campo1}")
        print(f"   campo2_sem_dv: {digitavel._campos.campo2_sem_dv}")
        print(f"   dv_campo2: {digitavel._campos.dv_campo2}")
        print(f"   campo3_sem_dv: {digitavel._campos.campo3_sem_dv}")
        print(f"   dv_campo3: {digitavel._campos.dv_campo3}")

        print(f"\n📊 PROPRIEDADES CALCULADAS:")
        print(f"   banco: {digitavel._campos.banco}")
        print(f"   moeda: {digitavel._campos.moeda}")
        print(f"   campo_livre: {digitavel._campos.campo_livre}")
        print(f"   fator_vencimento: {digitavel._campos.fator_vencimento}")
        print(f"   valor_centavos: {digitavel._campos.valor_centavos}")
        print(f"   valor_decimal: {digitavel._campos.valor_decimal}")
        print(f"   data_vencimento: {digitavel._campos.data_vencimento}")

    print(f"\n🎯 PROPRIEDADES PÚBLICAS:")
    print(f"   banco: {digitavel.banco}")
    print(f"   valor_documento: {digitavel.valor_documento}")
    print(f"   data_vencimento: {digitavel.data_vencimento}")
    print(f"   fator_vencimento: {digitavel.fator_vencimento}")
    print(f"   valor_centavos: {digitavel.valor_centavos}")
    print(f"   campo_livre: {digitavel.campo_livre}")
    print(f"   codigo_barras: {digitavel.codigo_barras}")

    print(f"\n🔧 MÉTODOS DE VALIDAÇÃO:")
    print(
        f"   _validar_campo(campo1): {digitavel._validar_campo(digitavel._campos.bloco_campo1) if digitavel._campos else False}"
    )
    print(
        f"   _validar_campo(campo2): {digitavel._validar_campo(digitavel._campos.bloco_campo2) if digitavel._campos else False}"
    )
    print(
        f"   _validar_campo(campo3): {digitavel._validar_campo(digitavel._campos.bloco_campo3) if digitavel._campos else False}"
    )
    print(
        f"   _validar_dv_geral: {digitavel._validar_dv_geral(digitavel.codigo_barras) if digitavel.codigo_barras else False}"
    )

    print(f"\n📋 MÉTODOS DE CÁLCULO:")
    print(
        f"   _calcular_modulo_10('033991614'): {digitavel._calcular_modulo_10('033991614')}"
    )
    print(
        f"   _calcular_modulo_11('0339916140700000192815560014411370000038936'): {digitavel._calcular_modulo_11('0339916140700000192815560014411370000038936')}"
    )

    print("=" * 60)


if __name__ == "__main__":
    print("🚀 Testando segunda camada da classe Digitavel\n")

    test_validacao_dv_completa()
    test_correcao_dv()
    test_geracao_codigo_barras()
    test_calculos_modulo()
    test_validacao_campos()
    test_digitavel_real_boleto_exemplo()
    test_digitavel_detalhado()
    test_nova_estrategia()
    test_linha_digitavel_real()
    exibir_objeto_digitavel()

    print("\n🎉 Todos os testes da segunda camada passaram!")
