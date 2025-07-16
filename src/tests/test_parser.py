#!/usr/bin/env python3
"""
Script de teste para o Boleto Parser
"""

import json
import sys
from pathlib import Path

from src.parser import BoletoParser


def test_parser():
    """Testa o parser com o arquivo de exemplo"""

    print("🧪 Testando Boleto Parser...")
    print("=" * 50)

    # Verificar se arquivo existe
    arquivo_teste = "boleto-exemplo.pdf"
    if not Path(arquivo_teste).exists():
        print(f"❌ Arquivo de teste não encontrado: {arquivo_teste}")
        return False

    try:
        # Criar parser
        parser = BoletoParser()

        print(f"📄 Processando arquivo: {arquivo_teste}")

        # Detectar tipo do arquivo
        tipo_arquivo = parser.detectar_tipo_arquivo(arquivo_teste)
        print(f"📋 Tipo do arquivo: {tipo_arquivo}")

        # Parse do boleto
        dados = parser.parse(arquivo_teste)

        print("Parse concluído com sucesso!")
        print(f"🎯 Tipo identificado: {dados.tipo_boleto}")
        print(f"💰 Valor: R$ {dados.valores.valor_documento:.2f}")
        print(f"📅 Vencimento: {dados.vencimento}")
        print(f"🏦 Beneficiário: {dados.beneficiario.nome}")
        print(f"👤 Pagador: {dados.pagador.nome}")

        if dados.aluno:
            print(f"🎓 Aluno: {dados.aluno.nome}")
            print(f"📚 Curso: {dados.aluno.curso}")

        # Salvar resultado em JSON
        resultado_json = dados.model_dump()
        with open("resultado_teste.json", "w", encoding="utf-8") as f:
            json.dump(resultado_json, f, ensure_ascii=False, indent=2)

        print(f"💾 Resultado salvo em: resultado_teste.json")

        # Mostrar estrutura do JSON
        print("\n📊 Estrutura dos dados extraídos:")
        print(json.dumps(resultado_json, ensure_ascii=False, indent=2))

        return True

    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_cli():
    """Testa a CLI"""
    print("\n🔧 Testando CLI...")
    print("=" * 30)

    try:
        import subprocess

        # Teste de validação
        resultado = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-m",
                "src.cli",
                "validate",
                "boleto-exemplo.pdf",
            ],
            capture_output=True,
            text=True,
        )

        if resultado.returncode == 0:
            print("✅ CLI de validação funcionando")
        else:
            print("❌ CLI de validação falhou")
            print(resultado.stderr)

        # Teste de extração de texto
        resultado = subprocess.run(
            [
                "poetry",
                "run",
                "python",
                "-m",
                "src.cli",
                "extract-text",
                "boleto-exemplo.pdf",
                "--output",
                "texto_teste.txt",
            ],
            capture_output=True,
            text=True,
        )

        if resultado.returncode == 0:
            print("✅ CLI de extração funcionando")
        else:
            print("❌ CLI de extração falhou")
            print(resultado.stderr)

    except Exception as e:
        print(f"❌ Erro ao testar CLI: {str(e)}")


if __name__ == "__main__":
    print("🚀 Iniciando testes do Boleto Parser")
    print("=" * 50)

    # Teste principal
    sucesso = test_parser()

    if sucesso:
        # Teste da CLI
        test_cli()

        print("\n🎉 Todos os testes concluídos!")
        print("📝 Para usar:")
        print("   CLI: poetry run python -m src.cli parse boleto-exemplo.pdf --pretty")
        print("   API: poetry run uvicorn src.api:app --host 0.0.0.0 --port 8000")
        print("   Docker: docker-compose up")
    else:
        print("\n💥 Testes falharam!")
        sys.exit(1)
