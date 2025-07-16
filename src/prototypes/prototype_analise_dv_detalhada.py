#!/usr/bin/env python3
"""
Protótipo: Análise Detalhada dos DVs
Debug completo dos cálculos de dígitos verificadores
"""

import re
from datetime import datetime, timedelta


def calcular_modulo_10_detalhado(numero: str) -> dict:
    """
    Calcula o DV Módulo 10 com detalhes completos
    """
    numero_invertido = numero[::-1]
    soma = 0
    detalhes = []

    print(f"   🔍 Cálculo Módulo 10 para: {numero}")
    print(f"   📋 Número invertido: {numero_invertido}")

    for i, digito in enumerate(numero_invertido):
        peso = 2 if i % 2 == 0 else 1
        resultado = int(digito) * peso

        # Se resultado > 9, soma os dígitos
        if resultado > 9:
            resultado_original = resultado
            resultado = sum(int(d) for d in str(resultado))
            detalhes.append(
                f"      {digito} × {peso} = {resultado_original} → {resultado}"
            )
        else:
            detalhes.append(f"      {digito} × {peso} = {resultado}")

        soma += resultado

    # Calcula o DV
    resto = soma % 10
    dv = 10 - resto
    if dv == 10:
        dv = 0

    resultado = {
        "numero": numero,
        "numero_invertido": numero_invertido,
        "detalhes": detalhes,
        "soma": soma,
        "resto": resto,
        "dv": dv,
    }

    return resultado


def calcular_modulo_11_detalhado(numero: str) -> dict:
    """
    Calcula o DV Módulo 11 com detalhes completos
    """
    numero_invertido = numero[::-1]
    soma = 0
    detalhes = []

    print(f"   🔍 Cálculo Módulo 11 para: {numero}")
    print(f"   📋 Número invertido: {numero_invertido}")

    for i, digito in enumerate(numero_invertido):
        peso = (i % 8) + 2  # Pesos de 2 a 9 (cíclicos)
        resultado = int(digito) * peso
        detalhes.append(f"      {digito} × {peso} = {resultado}")
        soma += resultado

    # Calcula o DV
    resto = soma % 11
    if resto == 0:
        dv = 1
    elif resto == 1:
        dv = 0
    else:
        dv = 11 - resto

    resultado = {
        "numero": numero,
        "numero_invertido": numero_invertido,
        "detalhes": detalhes,
        "soma": soma,
        "resto": resto,
        "dv": dv,
    }

    return resultado


def analisar_digitavel_detalhado(digitavel: str):
    """
    Análise detalhada do digitável com debug completo
    """
    print("🔍 ANÁLISE DETALHADA DO DIGITÁVEL")
    print(f"📝 Digitável: {digitavel}")

    # Remove espaços e pontos
    digitavel_limpo = re.sub(r"[.\s]", "", digitavel)
    print(f"🧹 Digitável limpo: {digitavel_limpo}")

    if len(digitavel_limpo) != 47:
        print(
            f"❌ ERRO: Digitável deve ter 47 dígitos, encontrado {len(digitavel_limpo)}"
        )
        return None

    try:
        print("\n📊 ANÁLISE DETALHADA:")
        print("=" * 50)

        # Campos da linha digitável
        campo1 = digitavel_limpo[0:10]  # AAABC.CCCCD
        campo2 = digitavel_limpo[10:20]  # DDDDE.EEEFF
        campo3 = digitavel_limpo[20:30]  # FFFFF.GGGGG
        campo4 = digitavel_limpo[30:31]  # H (DV geral)
        campo5 = digitavel_limpo[31:47]  # TTTTTTTTTT

        print("1️⃣ CAMPOS IDENTIFICADOS:")
        print(f"   📋 Campo 1: {campo1}")
        print(f"   📋 Campo 2: {campo2}")
        print(f"   📋 Campo 3: {campo3}")
        print(f"   📋 Campo 4: {campo4}")
        print(f"   📋 Campo 5: {campo5}")

        # 2. ANÁLISE DETALHADA CAMPO 1
        print("\n2️⃣ ANÁLISE DETALHADA CAMPO 1:")
        campo1_sem_dv = campo1[:-1]
        dv_campo1_esperado = campo1[-1]

        calc_campo1 = calcular_modulo_10_detalhado(campo1_sem_dv)
        print(f"   📋 Campo sem DV: {campo1_sem_dv}")
        for detalhe in calc_campo1["detalhes"]:
            print(detalhe)
        print(f"   📊 Soma: {calc_campo1['soma']}")
        print(f"   📊 Resto: {calc_campo1['resto']}")
        print(f"   🔢 DV Calculado: {calc_campo1['dv']}")
        print(f"   🔢 DV Esperado: {dv_campo1_esperado}")
        print(f"   ✅ Válido: {calc_campo1['dv'] == int(dv_campo1_esperado)}")

        # 3. ANÁLISE DETALHADA CAMPO 2
        print("\n3️⃣ ANÁLISE DETALHADA CAMPO 2:")
        campo2_sem_dv = campo2[:-1]
        dv_campo2_esperado = campo2[-1]

        calc_campo2 = calcular_modulo_10_detalhado(campo2_sem_dv)
        print(f"   📋 Campo sem DV: {campo2_sem_dv}")
        for detalhe in calc_campo2["detalhes"]:
            print(detalhe)
        print(f"   📊 Soma: {calc_campo2['soma']}")
        print(f"   📊 Resto: {calc_campo2['resto']}")
        print(f"   🔢 DV Calculado: {calc_campo2['dv']}")
        print(f"   🔢 DV Esperado: {dv_campo2_esperado}")
        print(f"   ✅ Válido: {calc_campo2['dv'] == int(dv_campo2_esperado)}")

        # 4. ANÁLISE DETALHADA CAMPO 3
        print("\n4️⃣ ANÁLISE DETALHADA CAMPO 3:")
        campo3_sem_dv = campo3[:-1]
        dv_campo3_esperado = campo3[-1]

        calc_campo3 = calcular_modulo_10_detalhado(campo3_sem_dv)
        print(f"   📋 Campo sem DV: {campo3_sem_dv}")
        for detalhe in calc_campo3["detalhes"]:
            print(detalhe)
        print("   📊 Soma: " + str(calc_campo3["soma"]))
        print("   📊 Resto: " + str(calc_campo3["resto"]))
        print("   🔢 DV Calculado: " + str(calc_campo3["dv"]))
        print("   🔢 DV Esperado: " + str(dv_campo3_esperado))
        print("   ✅ Válido: " + str(calc_campo3["dv"] == int(dv_campo3_esperado)))

        # 5. ANÁLISE DV GERAL
        print("\n5️⃣ ANÁLISE DV GERAL:")
        # Gera código de barras sem DV
        banco_moeda = digitavel_limpo[0:4]
        campo_livre = (
            digitavel_limpo[4:9] + digitavel_limpo[10:19] + digitavel_limpo[20:29]
        )
        fator_valor = digitavel_limpo[31:47]

        codigo_sem_dv = banco_moeda + campo_livre + fator_valor
        dv_geral_esperado = campo4

        calc_dv_geral = calcular_modulo_11_detalhado(codigo_sem_dv)
        print(f"   📊 Código sem DV: {codigo_sem_dv}")
        for detalhe in calc_dv_geral["detalhes"]:
            print(detalhe)
        print(f"   📊 Soma: {calc_dv_geral['soma']}")
        print(f"   📊 Resto: {calc_dv_geral['resto']}")
        print(f"   🔢 DV Calculado: {calc_dv_geral['dv']}")
        print(f"   🔢 DV Esperado: {dv_geral_esperado}")
        print(f"   ✅ Válido: {calc_dv_geral['dv'] == int(dv_geral_esperado)}")

        # 6. DECODIFICAÇÃO DOS CAMPOS
        print("\n6️⃣ DECODIFICAÇÃO DOS CAMPOS:")
        banco = campo1[0:3]
        moeda = campo1[3:4]
        campo_livre_1 = campo1[4:9]
        campo_livre_2 = campo2[0:9]
        campo_livre_3 = campo3[0:9]
        campo_livre_completo = campo_livre_1 + campo_livre_2 + campo_livre_3

        print(f"   🏦 Banco: {banco} ({identificar_banco(banco)})")
        print(f"   💰 Moeda: {moeda}")
        print(f"   📋 Campo Livre: {campo_livre_completo}")

        # 7. ANÁLISE CAMPO 5
        print("\n7️⃣ ANÁLISE CAMPO 5:")
        fator_vencimento = campo5[0:4]
        valor_centavos = campo5[4:14]

        try:
            fator_int = int(fator_vencimento)
            valor_int = int(valor_centavos)
            valor_decimal = valor_int / 100
            data_vencimento = fator_para_data(fator_int)

            print(f"   📅 Fator Vencimento: {fator_vencimento}")
            print(f"   💵 Valor (centavos): {valor_centavos}")
            print(f"   💵 Valor: R$ {valor_decimal:.2f}")
            print(f"   📅 Data Vencimento: {data_vencimento}")
        except Exception:
            print("   ⚠️  Erro na decodificação do Campo 5")

        # 8. RESUMO FINAL
        print("\n8️⃣ RESUMO FINAL:")
        campo1_valido = calc_campo1["dv"] == int(dv_campo1_esperado)
        campo2_valido = calc_campo2["dv"] == int(dv_campo2_esperado)
        campo3_valido = calc_campo3["dv"] == int(dv_campo3_esperado)
        dv_geral_valido = calc_dv_geral["dv"] == int(dv_geral_esperado)

        print(f"   ✅ Campo 1: {campo1_valido}")
        print(f"   ✅ Campo 2: {campo2_valido}")
        print(f"   ✅ Campo 3: {campo3_valido}")
        print(f"   ✅ DV Geral: {dv_geral_valido}")

        todos_validos = (
            campo1_valido and campo2_valido and campo3_valido and dv_geral_valido
        )
        print(f"   🎯 TODOS VÁLIDOS: {todos_validos}")

        if not todos_validos:
            print(f"\n⚠️  PROBLEMAS ENCONTRADOS:")
            if not campo2_valido:
                print(
                    f"   ❌ Campo 2: DV esperado {dv_campo2_esperado}, calculado {calc_campo2['dv']}"
                )
            if not campo3_valido:
                print(
                    f"   ❌ Campo 3: DV esperado {dv_campo3_esperado}, calculado {calc_campo3['dv']}"
                )
            if not dv_geral_valido:
                print(
                    f"   ❌ DV Geral: esperado {dv_geral_esperado}, calculado {calc_dv_geral['dv']}"
                )

        return {
            "campos_validos": {
                "campo1": campo1_valido,
                "campo2": campo2_valido,
                "campo3": campo3_valido,
                "dv_geral": dv_geral_valido,
            },
            "calculos": {
                "campo1": calc_campo1,
                "campo2": calc_campo2,
                "campo3": calc_campo3,
                "dv_geral": calc_dv_geral,
            },
            "todos_validos": todos_validos,
        }

    except Exception as e:
        print(f"❌ ERRO na análise: {e}")
        return None


def fator_para_data(fator: int) -> str:
    """Converte fator de vencimento para data"""
    data_base = datetime(1997, 10, 7)
    data_vencimento = data_base + timedelta(days=fator)
    return data_vencimento.strftime("%d/%m/%Y")


def identificar_banco(codigo: str) -> str:
    """Identifica o banco pelo código"""
    bancos = {
        "001": "Banco do Brasil",
        "033": "Santander",
        "104": "Caixa Econômica Federal",
        "237": "Bradesco",
        "341": "Itaú",
        "756": "Sicoob",
        "422": "Safra",
        "077": "Inter",
        "212": "Banco Original",
        "260": "Nu Pagamentos",
        "336": "C6 Bank",
        "655": "Banco Votorantim",
        "041": "Banrisul",
        "004": "Banco do Nordeste",
        "021": "Banestes",
        "047": "Banco do Estado de Sergipe",
        "085": "Cecred",
        "097": "Credisis",
        "136": "Unicred",
        "151": "Cooperativa Sicredi",
        "318": "Banco BMG",
        "356": "Banco Real",
        "389": "Banco Mercantil",
        "399": "HSBC",
        "633": "Banco Rendimento",
        "652": "Itaú Unibanco",
        "745": "Citibank",
        "748": "Sicredi",
    }
    return bancos.get(codigo, f"Banco {codigo}")


def testar_analise_detalhada():
    """Testa a análise detalhada"""
    print("🧪 TESTANDO ANÁLISE DETALHADA DOS DVs")
    print("=" * 70)

    # Digitável real
    digitavel_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"

    # Analisar
    resultado = analisar_digitavel_detalhado(digitavel_real)

    if resultado:
        print("\n📊 RESULTADO DA ANÁLISE:")
        print("=" * 50)

        # Status das validações
        print("🔍 STATUS DAS VALIDAÇÕES:")
        for campo, valido in resultado["campos_validos"].items():
            status = "✅" if valido else "❌"
            print(f"  {status} {campo}: {valido}")

        # Validação geral
        todos_validos = resultado["todos_validos"]
        print(
            f"\n🎯 VALIDAÇÃO GERAL: {'✅ TODOS VÁLIDOS' if todos_validos else '❌ ERROS ENCONTRADOS'}"
        )

        if not todos_validos:
            print(f"\n💡 SUGESTÕES:")
            print(f"   - Verificar se o digitável foi digitado corretamente")
            print(f"   - Confirmar se os campos estão sendo interpretados corretamente")
            print(
                f"   - Validar se o algoritmo de cálculo está correto para este banco"
            )

    else:
        print("\n❌ FALHA na análise")

    return resultado


if __name__ == "__main__":
    testar_analise_detalhada()
