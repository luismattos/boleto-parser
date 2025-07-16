#!/usr/bin/env python3
"""
Protótipo: Validação Completa dos Dígitos Verificadores
Implementação dos cálculos Módulo 10 e Módulo 11 da Febraban
"""

import re
from datetime import datetime, timedelta


def calcular_modulo_10(numero: str) -> int:
    """
    Calcula o dígito verificador usando Módulo 10

    Algoritmo:
    1. Multiplica cada dígito alternadamente por 2 e 1 (da direita para esquerda)
    2. Se o resultado > 9, soma os dígitos do resultado
    3. Soma todos os resultados
    4. DV = 10 - (soma % 10)
    """
    # Inverte para multiplicar da direita para esquerda
    numero_invertido = numero[::-1]
    soma = 0

    for i, digito in enumerate(numero_invertido):
        peso = 2 if i % 2 == 0 else 1
        resultado = int(digito) * peso

        # Se resultado > 9, soma os dígitos
        if resultado > 9:
            resultado = sum(int(d) for d in str(resultado))

        soma += resultado

    # Calcula o DV
    dv = 10 - (soma % 10)
    if dv == 10:
        dv = 0

    return dv


def calcular_modulo_11(numero: str) -> int:
    """
    Calcula o dígito verificador usando Módulo 11

    Algoritmo:
    1. Multiplica cada dígito por pesos de 2 a 9 (cíclicos, da direita para esquerda)
    2. Soma todos os resultados
    3. DV = 11 - (soma % 11)
    4. Se resultado for 0, 10 ou 11, DV = 1
    """
    # Inverte para multiplicar da direita para esquerda
    numero_invertido = numero[::-1]
    soma = 0

    for i, digito in enumerate(numero_invertido):
        peso = (i % 8) + 2  # Pesos de 2 a 9 (cíclicos)
        resultado = int(digito) * peso
        soma += resultado

    # Calcula o DV
    resto = soma % 11
    if resto == 0:
        dv = 1
    elif resto == 1:
        dv = 0
    else:
        dv = 11 - resto

    return dv


def validar_dv_campo(campo: str, dv_esperado: str) -> bool:
    """
    Valida o DV de um campo usando Módulo 10
    """
    # Remove o DV do campo para calcular
    campo_sem_dv = campo[:-1]
    dv_calculado = calcular_modulo_10(campo_sem_dv)
    dv_esperado_int = int(dv_esperado)

    return dv_calculado == dv_esperado_int


def validar_dv_geral(codigo_barras: str, dv_esperado: str) -> bool:
    """
    Valida o DV geral do código de barras usando Módulo 11
    """
    # Remove o DV do código de barras para calcular
    codigo_sem_dv = codigo_barras[:-1]
    dv_calculado = calcular_modulo_11(codigo_sem_dv)
    dv_esperado_int = int(dv_esperado)

    return dv_calculado == dv_esperado_int


def decodificar_com_validacao_dv(digitavel: str):
    """
    Decodifica o código digitável com validação completa dos DVs
    """
    print("🔍 DECODIFICAÇÃO COM VALIDAÇÃO DE DVs")
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
        print("\n📊 VALIDAÇÃO COMPLETA DOS DVs:")
        print("=" * 50)

        # Campos da linha digitável
        campo1 = digitavel_limpo[0:10]  # AAABC.CCCCD
        campo2 = digitavel_limpo[10:20]  # DDDDE.EEEFF
        campo3 = digitavel_limpo[20:30]  # FFFFF.GGGGG
        campo4 = digitavel_limpo[30:31]  # H (DV geral)
        campo5 = digitavel_limpo[31:47]  # TTTTTTTTTT

        print("1️⃣ VALIDAÇÃO DOS CAMPOS:")
        print(f"   📋 Campo 1: {campo1}")
        print(f"   📋 Campo 2: {campo2}")
        print(f"   📋 Campo 3: {campo3}")
        print(f"   📋 Campo 4: {campo4}")
        print(f"   📋 Campo 5: {campo5}")

        # 2. VALIDAÇÃO DV CAMPO 1
        print("\n2️⃣ VALIDAÇÃO DV CAMPO 1:")
        campo1_sem_dv = campo1[:-1]
        dv_campo1_esperado = campo1[-1]
        dv_campo1_calculado = calcular_modulo_10(campo1_sem_dv)
        campo1_valido = validar_dv_campo(campo1, dv_campo1_esperado)

        print(f"   📋 Campo sem DV: {campo1_sem_dv}")
        print(f"   🔢 DV Esperado: {dv_campo1_esperado}")
        print(f"   🔢 DV Calculado: {dv_campo1_calculado}")
        print(f"   ✅ Válido: {campo1_valido}")

        # 3. VALIDAÇÃO DV CAMPO 2
        print("\n3️⃣ VALIDAÇÃO DV CAMPO 2:")
        campo2_sem_dv = campo2[:-1]
        dv_campo2_esperado = campo2[-1]
        dv_campo2_calculado = calcular_modulo_10(campo2_sem_dv)
        campo2_valido = validar_dv_campo(campo2, dv_campo2_esperado)

        print(f"   📋 Campo sem DV: {campo2_sem_dv}")
        print(f"   🔢 DV Esperado: {dv_campo2_esperado}")
        print(f"   🔢 DV Calculado: {dv_campo2_calculado}")
        print(f"   ✅ Válido: {campo2_valido}")

        # 4. VALIDAÇÃO DV CAMPO 3
        print("\n4️⃣ VALIDAÇÃO DV CAMPO 3:")
        campo3_sem_dv = campo3[:-1]
        dv_campo3_esperado = campo3[-1]
        dv_campo3_calculado = calcular_modulo_10(campo3_sem_dv)
        campo3_valido = validar_dv_campo(campo3, dv_campo3_esperado)

        print(f"   📋 Campo sem DV: {campo3_sem_dv}")
        print(f"   🔢 DV Esperado: {dv_campo3_esperado}")
        print(f"   🔢 DV Calculado: {dv_campo3_calculado}")
        print(f"   ✅ Válido: {campo3_valido}")

        # 5. DECODIFICAÇÃO DOS CAMPOS
        print("\n5️⃣ DECODIFICAÇÃO DOS CAMPOS:")

        # Campo 1
        banco = campo1[0:3]
        moeda = campo1[3:4]
        campo_livre_1 = campo1[4:9]

        print(f"   🏦 Banco: {banco} ({identificar_banco(banco)})")
        print(f"   💰 Moeda: {moeda}")
        print(f"   📋 Campo Livre (parte 1): {campo_livre_1}")

        # Campo livre completo
        campo_livre_2 = campo2[0:9]
        campo_livre_3 = campo3[0:9]
        campo_livre_completo = campo_livre_1 + campo_livre_2 + campo_livre_3

        print(f"   📋 Campo Livre Completo: {campo_livre_completo}")

        # 6. VALIDAÇÃO DV GERAL (CAMPO 4)
        print("\n6️⃣ VALIDAÇÃO DV GERAL:")
        codigo_barras = gerar_codigo_barras_com_dv(digitavel_limpo)
        dv_geral_esperado = campo4
        dv_geral_calculado = calcular_modulo_11(codigo_barras[:-1])
        dv_geral_valido = validar_dv_geral(codigo_barras, dv_geral_esperado)

        print(f"   📊 Código de Barras: {codigo_barras}")
        print(f"   🔢 DV Geral Esperado: {dv_geral_esperado}")
        print(f"   🔢 DV Geral Calculado: {dv_geral_calculado}")
        print(f"   ✅ Válido: {dv_geral_valido}")

        # 7. DECODIFICAÇÃO CAMPO 5
        print("\n7️⃣ DECODIFICAÇÃO CAMPO 5:")
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

        # 8. VALIDAÇÃO FINAL
        print("\n8️⃣ VALIDAÇÃO FINAL:")
        todos_validos = (
            campo1_valido and campo2_valido and campo3_valido and dv_geral_valido
        )

        print(f"   ✅ Campo 1: {campo1_valido}")
        print(f"   ✅ Campo 2: {campo2_valido}")
        print(f"   ✅ Campo 3: {campo3_valido}")
        print(f"   ✅ DV Geral: {dv_geral_valido}")
        print(f"   🎯 TODOS VÁLIDOS: {todos_validos}")

        # 9. RESULTADO COMPLETO
        resultado = {
            "campos_digitavel": {
                "campo1": {
                    "banco": banco,
                    "nome_banco": identificar_banco(banco),
                    "moeda": moeda,
                    "campo_livre_parte1": campo_livre_1,
                    "dv_esperado": dv_campo1_esperado,
                    "dv_calculado": dv_campo1_calculado,
                    "valido": campo1_valido,
                },
                "campo2": {
                    "campo_livre_parte2": campo_livre_2,
                    "dv_esperado": dv_campo2_esperado,
                    "dv_calculado": dv_campo2_calculado,
                    "valido": campo2_valido,
                },
                "campo3": {
                    "campo_livre_parte3": campo_livre_3,
                    "dv_esperado": dv_campo3_esperado,
                    "dv_calculado": dv_campo3_calculado,
                    "valido": campo3_valido,
                },
                "campo4": {
                    "dv_geral_esperado": dv_geral_esperado,
                    "dv_geral_calculado": dv_geral_calculado,
                    "valido": dv_geral_valido,
                },
                "campo5": {
                    "fator_vencimento": fator_vencimento,
                    "valor_centavos": valor_centavos,
                    "valor_decimal": valor_decimal
                    if "valor_decimal" in locals()
                    else None,
                    "data_vencimento": data_vencimento
                    if "data_vencimento" in locals()
                    else None,
                },
            },
            "campo_livre": {
                "completo": campo_livre_completo,
                "parte1": campo_livre_1,
                "parte2": campo_livre_2,
                "parte3": campo_livre_3,
            },
            "validacoes": {
                "todos_validos": todos_validos,
                "codigo_barras": codigo_barras,
            },
            "digitavel_original": digitavel,
        }

        print("\n✅ VALIDAÇÃO COMPLETA CONCLUÍDA")
        return resultado

    except Exception as e:
        print(f"❌ ERRO na validação: {e}")
        return None


def gerar_codigo_barras_com_dv(digitavel: str) -> str:
    """Gera código de barras com DV"""
    # Código de barras = 44 dígitos + DV geral
    banco_moeda = digitavel[0:4]
    campo_livre = digitavel[4:9] + digitavel[10:19] + digitavel[20:29]
    fator_valor = digitavel[31:47]

    codigo_sem_dv = banco_moeda + campo_livre + fator_valor
    dv_geral = calcular_modulo_11(codigo_sem_dv)

    return codigo_sem_dv + str(dv_geral)


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


def testar_validacao_completa():
    """Testa a validação completa dos DVs"""
    print("🧪 TESTANDO VALIDAÇÃO COMPLETA DOS DVs")
    print("=" * 70)

    # Digitável real
    digitavel_real = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"

    # Validar
    resultado = decodificar_com_validacao_dv(digitavel_real)

    if resultado:
        print("\n📊 RESULTADO FINAL:")
        print("=" * 50)

        # Status das validações
        print("🔍 STATUS DAS VALIDAÇÕES:")
        for campo, dados in resultado["campos_digitavel"].items():
            if "valido" in dados:
                status = "✅" if dados["valido"] else "❌"
                print(f"  {status} {campo}: {dados['valido']}")

        # Validação geral
        todos_validos = resultado["validacoes"]["todos_validos"]
        print(
            f"\n🎯 VALIDAÇÃO GERAL: {'✅ TODOS VÁLIDOS' if todos_validos else '❌ ERROS ENCONTRADOS'}"
        )

        # Informações principais
        banco_info = resultado["campos_digitavel"]["campo1"]
        campo5_info = resultado["campos_digitavel"]["campo5"]

        print(f"\n🏦 INFORMAÇÕES PRINCIPAIS:")
        print(f"  Banco: {banco_info['banco']} ({banco_info['nome_banco']})")
        print(f"  Valor: R$ {campo5_info['valor_decimal']:.2f}")
        print(f"  Data: {campo5_info['data_vencimento']}")

        # Código de barras
        print(f"\n📊 CÓDIGO DE BARRAS: {resultado['validacoes']['codigo_barras']}")

    else:
        print("\n❌ FALHA na validação")

    return resultado


if __name__ == "__main__":
    testar_validacao_completa()
