#!/usr/bin/env python3
"""
Teste do protótipo V2 com texto real de boleto
"""

import json

from prototype_universal_parser_v2 import UniversalBoletoParserV2


def testar_com_texto_real():
    """Testa o protótipo V2 com texto real de boleto"""
    print("🧪 TESTANDO PROTÓTIPO V2 COM TEXTO REAL DE BOLETO")
    print("=" * 60)

    # Ler texto real do boleto
    with open("texto_completo.txt", "r", encoding="utf-8") as f:
        texto_real = f.read()

    # Remover logs do início do arquivo
    linhas = texto_real.split("\n")
    texto_limpo = []
    for linha in linhas:
        if not linha.startswith("[") and not linha.startswith("\x1b"):
            texto_limpo.append(linha)

    texto_boleto = "\n".join(texto_limpo)

    print(f"Texto extraído: {len(texto_boleto)} caracteres")
    print("Primeiras 200 caracteres:")
    print(texto_boleto[:200])
    print("...")

    # Criar instância do parser V2
    parser = UniversalBoletoParserV2()

    # Executar parsing universal
    resultado = parser.parse_universal(texto_boleto)

    # Exibir resultado
    print("\n📊 RESULTADO DO PARSING UNIVERSAL V2 COM TEXTO REAL:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Análise dos resultados
    print("\n🔍 ANÁLISE DOS RESULTADOS:")
    print(f"Campos obrigatórios encontrados: {len(resultado['campos_obrigatorios'])}")
    print(f"Campos opcionais encontrados: {len(resultado['campos_opcionais'])}")

    print("\nCampos obrigatórios encontrados:")
    for campo, valor in resultado["campos_obrigatorios"].items():
        print(f"  ✅ {campo}: {valor}")

    print("\nCampos opcionais encontrados:")
    for campo, valor in resultado["campos_opcionais"].items():
        print(f"  📝 {campo}: {valor}")

    return resultado


if __name__ == "__main__":
    testar_com_texto_real()
