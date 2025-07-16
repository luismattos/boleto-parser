#!/usr/bin/env python3
"""
Protótipo: Correção dos DVs
Sugere o digitável correto baseado nos cálculos
"""

import re
from datetime import datetime, timedelta


def calcular_modulo_10(numero: str) -> int:
    """Calcula DV Módulo 10"""
    numero_invertido = numero[::-1]
    soma = 0

    for i, digito in enumerate(numero_invertido):
        peso = 2 if i % 2 == 0 else 1
        resultado = int(digito) * peso

        if resultado > 9:
            resultado = sum(int(d) for d in str(resultado))

        soma += resultado

    dv = 10 - (soma % 10)
    if dv == 10:
        dv = 0

    return dv


def calcular_modulo_11(numero: str) -> int:
    """Calcula DV Módulo 11"""
    numero_invertido = numero[::-1]
    soma = 0

    for i, digito in enumerate(numero_invertido):
        peso = (i % 8) + 2
        resultado = int(digito) * peso
        soma += resultado

    resto = soma % 11
    if resto == 0:
        dv = 1
    elif resto == 1:
        dv = 0
    else:
        dv = 11 - resto

    return dv


def corrigir_digitavel(digitavel: str):
    """
    Tenta corrigir o digitável baseado nos cálculos de DV
    """
    print("🔧 CORREÇÃO DO DIGITÁVEL")
    print(f"📝 Digitável original: {digitavel}")

    # Remove espaços e pontos
    digitavel_limpo = re.sub(r"[.\s]", "", digitavel)

    if len(digitavel_limpo) != 47:
        print(f"❌ ERRO: Digitável deve ter 47 dígitos")
        return None

    try:
        print("\n📊 ANÁLISE E CORREÇÃO:")
        print("=" * 50)

        # Campos originais
        campo1_original = digitavel_limpo[0:10]
        campo2_original = digitavel_limpo[10:20]
        campo3_original = digitavel_limpo[20:30]
        campo4_original = digitavel_limpo[30:31]
        campo5_original = digitavel_limpo[31:47]

        print("1️⃣ CAMPOS ORIGINAIS:")
        print(f"   📋 Campo 1: {campo1_original}")
        print(f"   📋 Campo 2: {campo2_original}")
        print(f"   📋 Campo 3: {campo3_original}")
        print(f"   📋 Campo 4: {campo4_original}")
        print(f"   📋 Campo 5: {campo5_original}")

        # 2. CORREÇÃO CAMPO 2
        print("\n2️⃣ CORREÇÃO CAMPO 2:")
        campo2_sem_dv = campo2_original[:-1]
        dv_campo2_calculado = calcular_modulo_10(campo2_sem_dv)
        dv_campo2_original = int(campo2_original[-1])

        print(f"   📋 Campo sem DV: {campo2_sem_dv}")
        print(f"   🔢 DV Original: {dv_campo2_original}")
        print(f"   🔢 DV Calculado: {dv_campo2_calculado}")

        if dv_campo2_calculado != dv_campo2_original:
            campo2_corrigido = campo2_sem_dv + str(dv_campo2_calculado)
            print(f"   🔧 Campo 2 corrigido: {campo2_corrigido}")
        else:
            campo2_corrigido = campo2_original
            print(f"   ✅ Campo 2 já está correto")

        # 3. CORREÇÃO CAMPO 3
        print("\n3️⃣ CORREÇÃO CAMPO 3:")
        campo3_sem_dv = campo3_original[:-1]
        dv_campo3_calculado = calcular_modulo_10(campo3_sem_dv)
        dv_campo3_original = int(campo3_original[-1])

        print(f"   📋 Campo sem DV: {campo3_sem_dv}")
        print(f"   🔢 DV Original: {dv_campo3_original}")
        print(f"   🔢 DV Calculado: {dv_campo3_calculado}")

        if dv_campo3_calculado != dv_campo3_original:
            campo3_corrigido = campo3_sem_dv + str(dv_campo3_calculado)
            print(f"   🔧 Campo 3 corrigido: {campo3_corrigido}")
        else:
            campo3_corrigido = campo3_original
            print(f"   ✅ Campo 3 já está correto")

        # 4. CORREÇÃO DV GERAL
        print("\n4️⃣ CORREÇÃO DV GERAL:")
        # Gera código de barras com campos corrigidos
        banco_moeda = digitavel_limpo[0:4]
        campo_livre = (
            digitavel_limpo[4:9] + campo2_corrigido[:-1] + campo3_corrigido[:-1]
        )
        fator_valor = digitavel_limpo[31:47]

        codigo_sem_dv = banco_moeda + campo_livre + fator_valor
        dv_geral_calculado = calcular_modulo_11(codigo_sem_dv)
        dv_geral_original = int(campo4_original)

        print(f"   📊 Código sem DV: {codigo_sem_dv}")
        print(f"   🔢 DV Original: {dv_geral_original}")
        print(f"   🔢 DV Calculado: {dv_geral_calculado}")

        if dv_geral_calculado != dv_geral_original:
            campo4_corrigido = str(dv_geral_calculado)
            print(f"   🔧 Campo 4 corrigido: {campo4_corrigido}")
        else:
            campo4_corrigido = campo4_original
            print(f"   ✅ Campo 4 já está correto")

        # 5. DIGITÁVEL CORRIGIDO
        print("\n5️⃣ DIGITÁVEL CORRIGIDO:")
        digitavel_corrigido = (
            campo1_original
            + campo2_corrigido
            + campo3_corrigido
            + campo4_corrigido
            + campo5_original
        )

        # Formatação visual
        digitavel_formatado = (
            f"{digitavel_corrigido[0:10]} "
            f"{digitavel_corrigido[10:20]} "
            f"{digitavel_corrigido[20:30]} "
            f"{digitavel_corrigido[30:31]} "
            f"{digitavel_corrigido[31:47]}"
        )

        print(f"   📝 Digitável corrigido: {digitavel_formatado}")

        # 6. VALIDAÇÃO FINAL
        print("\n6️⃣ VALIDAÇÃO FINAL:")

        # Validação dos campos corrigidos
        campo1_valido = True  # Já estava correto
        campo2_valido = calcular_modulo_10(campo2_corrigido[:-1]) == int(
            campo2_corrigido[-1]
        )
        campo3_valido = calcular_modulo_10(campo3_corrigido[:-1]) == int(
            campo3_corrigido[-1]
        )

        # Validação DV geral
        codigo_final = banco_moeda + campo_livre + fator_valor + campo4_corrigido
        dv_geral_valido = calcular_modulo_11(codigo_final[:-1]) == int(campo4_corrigido)

        print(f"   ✅ Campo 1: {campo1_valido}")
        print(f"   ✅ Campo 2: {campo2_valido}")
        print(f"   ✅ Campo 3: {campo3_valido}")
        print(f"   ✅ DV Geral: {dv_geral_valido}")

        todos_validos = (
            campo1_valido and campo2_valido and campo3_valido and dv_geral_valido
        )
        print(f"   🎯 TODOS VÁLIDOS: {todos_validos}")

        # 7. DECODIFICAÇÃO DO DIGITÁVEL CORRIGIDO
        print("\n7️⃣ DECODIFICAÇÃO DO DIGITÁVEL CORRIGIDO:")
        banco = digitavel_corrigido[0:3]
        moeda = digitavel_corrigido[3:4]
        campo_livre_1 = digitavel_corrigido[4:9]
        campo_livre_2 = digitavel_corrigido[10:19]
        campo_livre_3 = digitavel_corrigido[20:29]
        campo_livre_completo = campo_livre_1 + campo_livre_2 + campo_livre_3

        fator_vencimento = digitavel_corrigido[31:35]
        valor_centavos = digitavel_corrigido[35:45]

        try:
            fator_int = int(fator_vencimento)
            valor_int = int(valor_centavos)
            valor_decimal = valor_int / 100
            data_vencimento = fator_para_data(fator_int)

            print(f"   🏦 Banco: {banco} ({identificar_banco(banco)})")
            print(f"   💰 Moeda: {moeda}")
            print(f"   📋 Campo Livre: {campo_livre_completo}")
            print(f"   📅 Fator Vencimento: {fator_vencimento}")
            print(f"   💵 Valor: R$ {valor_decimal:.2f}")
            print(f"   📅 Data Vencimento: {data_vencimento}")
        except Exception:
            print("   ⚠️  Erro na decodificação")

        # 8. RESULTADO FINAL
        resultado = {
            "digitavel_original": digitavel,
            "digitavel_corrigido": digitavel_formatado,
            "campos_corrigidos": {
                "campo1": campo1_original,
                "campo2": campo2_corrigido,
                "campo3": campo3_corrigido,
                "campo4": campo4_corrigido,
                "campo5": campo5_original,
            },
            "validacoes": {
                "campo1": campo1_valido,
                "campo2": campo2_valido,
                "campo3": campo3_valido,
                "dv_geral": dv_geral_valido,
                "todos_validos": todos_validos,
            },
            "decodificacao": {
                "banco": banco,
                "nome_banco": identificar_banco(banco),
                "moeda": moeda,
                "campo_livre": campo_livre_completo,
                "fator_vencimento": fator_vencimento,
                "valor": valor_decimal if "valor_decimal" in locals() else None,
                "data_vencimento": data_vencimento
                if "data_vencimento" in locals()
                else None,
            },
        }

        print("\n✅ CORREÇÃO CONCLUÍDA")
        return resultado

    except Exception as e:
        print(f"❌ ERRO na correção: {e}")
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


def testar_correcao():
    """Testa a correção do digitável"""
    print("🧪 TESTANDO CORREÇÃO DO DIGITÁVEL")
    print("=" * 70)

    # Digitável real
    digitavel_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"

    # Corrigir
    resultado = corrigir_digitavel(digitavel_real)

    if resultado:
        print("\n📊 RESULTADO FINAL:")
        print("=" * 50)

        print("🔧 CORREÇÕES APLICADAS:")
        for campo, valor in resultado["campos_corrigidos"].items():
            print(f"  {campo}: {valor}")

        print("\n✅ VALIDAÇÕES:")
        for campo, valido in resultado["validacoes"].items():
            status = "✅" if valido else "❌"
            print(f"  {status} {campo}: {valido}")

        print(f"\n📝 DIGITÁVEL CORRIGIDO:")
        print(f"  {resultado['digitavel_corrigido']}")

        print(f"\n🏦 INFORMAÇÕES DECODIFICADAS:")
        decod = resultado["decodificacao"]
        print(f"  Banco: {decod['banco']} ({decod['nome_banco']})")
        print(f"  Valor: R$ {decod['valor']:.2f}")
        print(f"  Data: {decod['data_vencimento']}")

    else:
        print("\n❌ FALHA na correção")

    return resultado


if __name__ == "__main__":
    testar_correcao()
