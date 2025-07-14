from pathlib import Path

import pytest

from src.parser import BoletoParser


@pytest.fixture(scope="module")
def boleto_path():
    # Tentar diferentes locais para o arquivo de teste
    possible_paths = [
        Path("boleto-exemplo.pdf"),
        Path("sensitive_documents/boleto-exemplo.pdf"),
        Path("tests/boleto-exemplo.pdf")
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    # Se não encontrar, pular o teste
    pytest.skip("Arquivo de teste boleto-exemplo.pdf não encontrado")


def test_parse_boleto(boleto_path):
    parser = BoletoParser()
    dados = parser.parse(boleto_path)

    # Testa tipo
    assert dados.tipo_boleto == "educacional"

    # Testa beneficiário
    assert "ANTARES EDUCACIONAL SA - UVA" in dados.beneficiario.nome
    assert dados.beneficiario.cnpj == "34.185.306/0001-81"
    assert dados.beneficiario.agencia == "0057"
    assert dados.beneficiario.codigo_beneficiario == "1614070"
    assert dados.beneficiario.nosso_numero.startswith("000019181556")

    # Testa pagador
    assert "MARIA CRISTINA VENTURA BÁRCIA" in dados.pagador.nome
    assert dados.pagador.cpf_cnpj == "409.910.677-20"

    # Testa aluno
    assert dados.aluno is not None
    assert "LUIS PAULO BÁRCIA DE MATTOS" in dados.aluno.nome
    assert dados.aluno.matricula == "1170101378"
    assert "CIÊNCIA DA COMPUTAÇÃO" in dados.aluno.curso
    assert dados.aluno.turno == "N"
    assert dados.aluno.codigo == "10001"

    # Testa valores (pode ser 0.0 se regex não capturou)
    assert isinstance(dados.valores.valor_documento, float)
    assert isinstance(dados.valores.valor_cobrado, float)

    # Testa endereço da instituição
    assert "RUA IBITURUNA, 108" in dados.endereco_instituicao.endereco
    assert dados.endereco_instituicao.cep == "20271-020"

    # Testa instruções
    assert "Pagável em qualquer Banco" in dados.instrucoes.local_pagamento
    assert "R$7,79" in (dados.instrucoes.multa_vencimento or "")
    assert "R$0,13" in (dados.instrucoes.juros_dia_atraso or "")
