#!/usr/bin/env python3
"""
Teste simples para a classe BoletoBancario
"""

from datetime import datetime

from src.boleto import BoletoBancario


def test_classe_boleto():
    """Testa a classe BoletoBancario"""
    print("🧪 TESTANDO CLASSE BOLETO BANCÁRIO")
    print("=" * 70)

    # Criar boleto de exemplo
    boleto = BoletoBancario(
        # Campos obrigatórios
        codigo_banco="033",
        linha_digitavel="033991614.0 0700000191.2 8155600101.4 4 11370000038936",
        codigo_barras="0339916140700000192815560014411370000038936",
        nome_cedente="EMPRESA EXEMPLO LTDA",
        cnpj_cpf_cedente="12.345.678/0001-90",
        nome_pagador="CLIENTE EXEMPLO",
        cnpj_cpf_pagador="123.456.789-00",
        data_vencimento=datetime(2025, 7, 9),
        valor_documento=389.36,
        nosso_numero="123456789",
        carteira="101",
        data_emissao=datetime(2025, 6, 9),
        # Campos opcionais
        agencia_cedente="1234",
        conta_cedente="12345-6",
        codigo_beneficiario="123456",
        instrucoes=[
            "Após o vencimento, cobrar multa de 2% e juros de 0,033% ao dia",
            "Não receber após 30 dias do vencimento",
        ],
        desconto_valor=10.00,
        desconto_data=datetime(2025, 7, 5),
        juros_percentual=0.033,
        multa_percentual=2.0,
        numero_documento="FAT-2025-001",
        informacoes_adicionais=[
            "Referente à fatura FAT-2025-001",
            "Em caso de dúvidas, entre em contato",
        ],
        protesto_dias=30,
        endereco_cedente="Rua Exemplo, 123 - Centro - São Paulo/SP",
        endereco_pagador="Rua Cliente, 456 - Bairro - São Paulo/SP",
    )

    print("📊 INFORMAÇÕES DO BOLETO:")
    print(f"   {boleto}")

    print("\n🏦 CAMPOS OBRIGATÓRIOS:")
    print(f"   Código Banco: {boleto.codigo_banco}")
    print(f"   Linha Digitável: {boleto.linha_digitavel}")
    print(f"   Código de Barras: {boleto.codigo_barras}")
    print(f"   Cedente: {boleto.nome_cedente}")
    print(f"   CNPJ/CPF Cedente: {boleto.cnpj_cpf_cedente}")
    print(f"   Pagador: {boleto.nome_pagador}")
    print(f"   CNPJ/CPF Pagador: {boleto.cnpj_cpf_pagador}")
    print(f"   Vencimento: {boleto.data_vencimento.strftime('%d/%m/%Y')}")
    print(f"   Valor: R$ {boleto.valor_documento:.2f}")
    print(f"   Nosso Número: {boleto.nosso_numero}")
    print(f"   Carteira: {boleto.carteira}")
    print(f"   Emissão: {boleto.data_emissao.strftime('%d/%m/%Y')}")
    print(f"   Espécie: {boleto.especie_documento.value}")
    print(f"   Aceite: {boleto.aceite.value}")

    print("\n📝 CAMPOS OPCIONAIS:")
    print(f"   Agência: {boleto.agencia_cedente}")
    print(f"   Conta: {boleto.conta_cedente}")
    print(f"   Código Beneficiário: {boleto.codigo_beneficiario}")
    print(f"   Instruções: {len(boleto.instrucoes)} instruções")
    for i, instrucao in enumerate(boleto.instrucoes, 1):
        print(f"     {i}. {instrucao}")

    if boleto.desconto_valor:
        print(f"   Desconto: R$ {boleto.desconto_valor:.2f}")
    if boleto.juros_percentual:
        print(f"   Juros: {boleto.juros_percentual}% ao dia")
    if boleto.multa_percentual:
        print(f"   Multa: {boleto.multa_percentual}%")

    print(f"   Local Pagamento: {boleto.local_pagamento}")
    print(f"   Endereço Cedente: {boleto.endereco_cedente}")
    print(f"   Endereço Pagador: {boleto.endereco_pagador}")

    print("\n✅ VALIDAÇÃO:")
    valido = boleto.validar_campos_obrigatorios()
    print(f"   Campos Obrigatórios Válidos: {valido}")

    return boleto


if __name__ == "__main__":
    test_classe_boleto()
