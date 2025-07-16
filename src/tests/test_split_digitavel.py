#!/usr/bin/env python3
"""
Teste para mostrar exatamente como está sendo feito o split da linha digitável
"""

from ..core.digitavel import Digitavel


def test_split_digitavel():
    """Mostra exatamente como está sendo feito o split"""
    print("🔍 ANÁLISE DO SPLIT DA LINHA DIGITÁVEL")
    print("=" * 50)

    # Linha digitável fornecida pelo usuário
    linha_original = "033991614.0 0700000191.2 8155600101.4 4 11370000038936"
    print(f"📝 Linha original: {linha_original}")

    # Normalização
    linha_normalizada = linha_original.replace(" ", "").replace(".", "")
    print(f"🧹 Linha normalizada: {linha_normalizada}")
    print(f"📏 Tamanho: {len(linha_normalizada)} dígitos")

    # Split manual para mostrar exatamente como está sendo feito
    campo1 = linha_normalizada[0:10]
    campo2 = linha_normalizada[10:21]
    campo3 = linha_normalizada[21:32]
    campo4 = linha_normalizada[32:33]
    campo5 = linha_normalizada[33:47]

    print("\nSPLIT MANUAL:")
    print(f"  Campo 1 (0:10):   {campo1} | Tamanho: {len(campo1)}")
    print(f"  Campo 2 (10:21):  {campo2} | Tamanho: {len(campo2)}")
    print(f"  Campo 3 (21:32):  {campo3} | Tamanho: {len(campo3)}")
    print(f"  Campo 4 (32:33):  {campo4} | Tamanho: {len(campo4)}")
    print(f"  Campo 5 (33:47):  {campo5} | Tamanho: {len(campo5)}")

    # Teste com a classe Digitavel
    digitavel = Digitavel(linha_original)
    print(f"\n🏗️  OBJETO DIGITAVEL:")
    if digitavel._campos:
        print(f"  bloco_campo1: {digitavel._campos.bloco_campo1}")
        print(f"  bloco_campo2: {digitavel._campos.bloco_campo2}")
        print(f"  bloco_campo3: {digitavel._campos.bloco_campo3}")
        print(f"  dv_geral: {digitavel._campos.dv_geral}")
        print(f"  fator_valor_e_valor: {digitavel._campos.fator_valor_e_valor}")
    else:
        print("Campo 1 inválido")
        print("Campo 2 inválido")

    print("=" * 50)


def validar_campos_digitavel(linha):
    from ..core.digitavel import Digitavel

    digitavel = Digitavel(linha)
    print("\n🔎 VALIDAÇÃO DOS CAMPOS:")
    if digitavel._campos:
        c1 = digitavel._campos.bloco_campo1
        c2 = digitavel._campos.bloco_campo2
        c3 = digitavel._campos.bloco_campo3
        dv_geral = digitavel._campos.dv_geral
        print(f"  Campo 1: {c1} | DV correto? {digitavel._validar_campo(c1)}")
        print(f"  Campo 2: {c2} | DV correto? {digitavel._validar_campo(c2)}")
        print(f"  Campo 3: {c3} | DV correto? {digitavel._validar_campo(c3)}")
        # Código de barras para DV geral
        codigo_barras = digitavel.codigo_barras
        print(
            f"  DV Geral: {dv_geral} | DV correto? {digitavel._validar_dv_geral(codigo_barras) if codigo_barras else False}"
        )
        print(f"  Código de barras: {codigo_barras}")
    else:
        print("  Não foi possível extrair os campos.")


if __name__ == "__main__":
    test_split_digitavel()
    validar_campos_digitavel("033991614.0 0700000191.2 8155600101.4 4 11370000038936")
