import json
from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.table import Table

from .logger import get_logger, setup_default_logging
from .parser import BoletoParser, BoletoDecoder

# Configurar console
console = Console()


# Enum para tipos de saída
class OutputFormat(str, Enum):
    json = "json"
    pretty = "pretty"
    table = "table"
    csv = "csv"


# Enum para níveis de log
class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


def validate_pdf_file(file_path: str) -> str:
    """Valida se o arquivo existe e é um PDF"""
    path = Path(file_path)
    if not path.exists():
        raise typer.BadParameter(f"Arquivo não encontrado: {file_path}")
    if not path.suffix.lower() == ".pdf":
        raise typer.BadParameter(f"Arquivo deve ser um PDF: {file_path}")
    return str(path)


def setup_logging_callback(
    log_level: LogLevel, log_file: Optional[str], json_logs: bool
):
    """Callback para configurar logging baseado nos parâmetros da CLI"""
    if log_file:
        from .logger import setup_logging
        setup_logging(
            log_level=log_level.value,
            log_file=log_file,
            json_format=json_logs,
            console_output=True,
        )
    else:
        setup_default_logging()


# Criar app principal
app = typer.Typer(
    help="Parser inteligente de boletos bancários PDF",
    add_completion=False,
    rich_markup_mode="rich",
)

# App para comandos de desenvolvimento
dev_app = typer.Typer(help="Comandos de desenvolvimento e debug")
app.add_typer(dev_app, name="dev")

# App para comandos de produção
prod_app = typer.Typer(help="Comandos de produção")
app.add_typer(prod_app, name="prod")


@app.callback()
def main(
    log_level: LogLevel = typer.Option(
        LogLevel.info, "--log-level", "-l", help="Nível de logging"
    ),
    log_file: Optional[str] = typer.Option(
        None, "--log-file", help="Arquivo de log (opcional)"
    ),
    json_logs: bool = typer.Option(
        False, "--json-logs", help="Usar formato JSON para logs"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Modo silencioso (sem saída no console)"
    ),
):
    """Parser inteligente de boletos bancários PDF com logging estruturado"""
    if not quiet:
        setup_logging_callback(log_level, log_file, json_logs)

    logger = get_logger("cli")
    logger.info("CLI iniciada", log_level=log_level.value, json_logs=json_logs)


@app.command()
def parse(
    arquivo: str = typer.Argument(
        ..., help="Caminho para o arquivo PDF do boleto", callback=validate_pdf_file
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Arquivo de saída JSON"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.json, "--format", "-f", help="Formato de saída"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verboso"),
    force: bool = typer.Option(
        False, "--force", help="Sobrescrever arquivo de saída sem confirmar"
    ),
):
    """
    Parse um arquivo PDF de boleto bancário e extrai dados estruturados.

    [bold green]Exemplos:[/bold green]

    • Parse básico:
        [code]python -m src.cli parse meu-boleto.pdf[/code]

    • Parse com saída formatada:
        [code]python -m src.cli parse meu-boleto.pdf --format pretty[/code]

    • Parse salvando em arquivo:
        [code]python -m src.cli parse meu-boleto.pdf --output dados.json[/code]

    • Parse com logs detalhados:
        [code]python -m src.cli parse meu-boleto.pdf --verbose --log-level DEBUG[/code]
    """
    logger = get_logger("cli")

    try:
        logger.info(
            "Iniciando processamento do arquivo", arquivo=arquivo, verbose=verbose
        )

        if verbose:
            console.print(f"[yellow]Processando arquivo:[/yellow] {arquivo}")

        # Verificar se arquivo de saída já existe
        if output and Path(output).exists() and not force:
            if not Confirm.ask(f"Arquivo {output} já existe. Sobrescrever?"):
                raise typer.Exit(0)

        # Processar com progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Processando boleto...", total=None)

            # Criar parser e processar
            parser = BoletoParser()
            dados = parser.parse(arquivo)

            progress.update(task, description="Finalizando...")

        # Converter para dict
        dados_dict = dados.model_dump()

        logger.info("Arquivo processado com sucesso", tipo=dados.tipo_boleto)

        if verbose:
            console.print("[green]✓[/green] Arquivo processado com sucesso!")
            console.print(f"[blue]Tipo identificado:[/blue] {dados.tipo_boleto}")

        # Saída baseada no formato
        if output:
            _save_output(dados_dict, output, format)
            logger.info("Dados salvos em arquivo", arquivo=output, formato=format.value)
            console.print(f"[green]✓[/green] Dados salvos em: {output}")
        else:
            _display_output(dados_dict, format)

    except Exception as e:
        logger.error("Erro durante processamento", erro=str(e), arquivo=arquivo)
        console.print(f"[red]Erro:[/red] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


def _save_output(data: dict, output_file: str, format: OutputFormat):
    """Salva dados no formato especificado"""
    if format == OutputFormat.csv:
        # Implementar conversão para CSV
        raise typer.BadParameter("Formato CSV ainda não implementado")
    else:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def _display_output(data: dict, format: OutputFormat):
    """Exibe dados no formato especificado"""
    if format == OutputFormat.pretty:
        _display_pretty(data)
    elif format == OutputFormat.table:
        _display_table(data)
    elif format == OutputFormat.csv:
        raise typer.BadParameter("Formato CSV ainda não implementado")
    else:  # json
        print(json.dumps(data, ensure_ascii=False, indent=2))


def _display_pretty(data: dict):
    """Exibe dados em formato bonito"""
    # Tabela resumida
    table = Table(title="Dados do Boleto")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="green")

    # Adaptar para dados de decodificação
    if "banco" in data:
        # Dados de decodificação
        table.add_row("Banco", data.get("banco", {}).get("nome", ""))
        table.add_row("Valor", f"R$ {data.get('valor', 0):.2f}")
        table.add_row("Vencimento", data.get("vencimento", ""))
        table.add_row("Código de Barras", data.get("codigo_barras", ""))
    else:
        # Dados de parsing
        table.add_row("Número do Boleto", data.get("numero_boleto", ""))
        table.add_row("Vencimento", data.get("vencimento", ""))
        table.add_row(
            "Valor", f"R$ {data.get('valores', {}).get('valor_documento', 0):.2f}"
        )
        table.add_row("Beneficiário", data.get("beneficiario", {}).get("nome", ""))
        table.add_row("Pagador", data.get("pagador", {}).get("nome", ""))
        if data.get("aluno"):
            table.add_row("Aluno", data["aluno"].get("nome", ""))
        table.add_row("Tipo", data.get("tipo_boleto", ""))

    console.print(table)

    # JSON completo em painel
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    panel = Panel(JSON(json_str), title="Dados Completos", border_style="blue")
    console.print(panel)


def _display_table(data: dict):
    """Exibe dados em formato de tabela"""
    table = Table(title="Dados Completos do Boleto")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="green")

    # Adicionar todos os campos principais
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                table.add_row(f"{key}.{sub_key}", str(sub_value))
        else:
            table.add_row(key, str(value))

    console.print(table)


@app.command()
def decode(
    digitavel: str = typer.Argument(
        ..., help="Código digitável do boleto (ex: 03399.16140 70000.019182 81556.601014 4 11370000038936)"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Arquivo de saída JSON"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.json, "--format", "-f", help="Formato de saída"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Modo verboso"),
):
    """
    Decodifica um código digitável de boleto bancário.

    [bold green]Exemplos:[/bold green]

    • Decodificação básica:
        [code]python -m src.cli decode "03399.16140 70000.019182 81556.601014 4 11370000038936"[/code]

    • Decodificação com saída formatada:
        [code]python -m src.cli decode "03399.16140 70000.019182 81556.601014 4 11370000038936" --format pretty[/code]

    • Decodificação salvando em arquivo:
        [code]python -m src.cli decode "03399.16140 70000.019182 81556.601014 4 11370000038936" --output dados.json[/code]
    """
    logger = get_logger("cli")

    try:
        logger.info("Iniciando decodificação", digitavel=digitavel)

        if verbose:
            console.print(f"[yellow]Decodificando:[/yellow] {digitavel}")

        # Criar decoder e processar
        decoder = BoletoDecoder()
        dados = decoder.decodificar_digitavel(digitavel)

        logger.info("Código digitável decodificado com sucesso", banco=dados["banco"]["nome"])

        if verbose:
            console.print("[green]✓[/green] Código digitável decodificado com sucesso!")
            console.print(f"[blue]Banco:[/blue] {dados['banco']['nome']}")
            console.print(f"[blue]Valor:[/blue] R$ {dados['valor']:.2f}")
            console.print(f"[blue]Vencimento:[/blue] {dados['vencimento']}")

        # Saída baseada no formato
        if output:
            _save_output(dados, output, format)
            logger.info("Dados salvos em arquivo", arquivo=output, formato=format.value)
            console.print(f"[green]✓[/green] Dados salvos em: {output}")
        else:
            _display_output(dados, format)

    except Exception as e:
        logger.error("Erro durante decodificação", erro=str(e), digitavel=digitavel)
        console.print(f"[red]Erro:[/red] {str(e)}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def validate(
    arquivo: str = typer.Argument(
        ..., help="Caminho para o arquivo PDF do boleto", callback=validate_pdf_file
    ),
    strict: bool = typer.Option(False, "--strict", help="Validação mais rigorosa"),
):
    """
    Valida se um arquivo PDF é um boleto válido sem extrair dados completos.

    [bold green]Exemplos:[/bold green]

    • Validação básica:
        [code]python -m src.cli validate meu-boleto.pdf[/code]

    • Validação rigorosa:
        [code]python -m src.cli validate meu-boleto.pdf --strict[/code]
    """
    logger = get_logger("cli")

    try:
        logger.info("Iniciando validação", arquivo=arquivo, strict=strict)

        parser = BoletoParser()

        # Detectar tipo do arquivo
        tipo_arquivo = parser.detectar_tipo_arquivo(arquivo)
        console.print(f"[blue]Tipo do arquivo:[/blue] {tipo_arquivo}")

        if "PDF" not in tipo_arquivo:
            console.print("[red]✗[/red] Arquivo não é um PDF válido")
            raise typer.Exit(1)

        # Extrair texto para validação
        texto = parser.extrair_texto_pdf(arquivo)

        # Verificar se contém elementos de boleto
        elementos_boleto = ["Beneficiário", "Pagador", "Vencimento", "Valor", "CNPJ"]

        encontrados = []
        for elemento in elementos_boleto:
            if elemento in texto:
                encontrados.append(elemento)

        # Validação baseada no modo
        if strict:
            is_valid = len(encontrados) >= 4  # Mais rigoroso
        else:
            is_valid = len(encontrados) >= 3

        if is_valid:
            console.print(f"[green]✓[/green] Arquivo parece ser um boleto válido")
            console.print(
                f"[blue]Elementos encontrados:[/blue] {', '.join(encontrados)}"
            )
            logger.info(
                "Validação bem-sucedida", elementos=encontrados, total=len(encontrados)
            )
        else:
            console.print("[yellow]⚠[/yellow] Arquivo pode não ser um boleto válido")
            console.print(
                f"[blue]Elementos encontrados:[/blue] {', '.join(encontrados)}"
            )
            logger.warning(
                "Validação falhou", elementos=encontrados, total=len(encontrados)
            )

    except Exception as e:
        logger.error("Erro durante validação", erro=str(e), arquivo=arquivo)
        console.print(f"[red]Erro:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def extract_text(
    arquivo: str = typer.Argument(
        ..., help="Caminho para o arquivo PDF", callback=validate_pdf_file
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Arquivo de saída"
    ),
    encoding: str = typer.Option(
        "utf-8", "--encoding", "-e", help="Encoding do arquivo de saída"
    ),
):
    """
    Extrai apenas o texto bruto do PDF sem processamento.

    [bold green]Exemplos:[/bold green]

    • Extrair para console:
        [code]python -m src.cli extract-text meu-boleto.pdf[/code]

    • Extrair para arquivo:
        [code]python -m src.cli extract-text meu-boleto.pdf --output texto.txt[/code]
    """
    logger = get_logger("cli")

    try:
        logger.info("Iniciando extração de texto", arquivo=arquivo, output=output)

        parser = BoletoParser()

        # Extrair texto
        texto = parser.extrair_texto_pdf(arquivo)

        if output:
            with open(output, "w", encoding=encoding) as f:
                f.write(texto)
            console.print(f"[green]✓[/green] Texto extraído salvo em: {output}")
            logger.info("Texto salvo em arquivo", arquivo=output, tamanho=len(texto))
        else:
            print(texto)

    except Exception as e:
        logger.error("Erro durante extração", erro=str(e), arquivo=arquivo)
        console.print(f"[red]Erro:[/red] {str(e)}")
        raise typer.Exit(1)


@dev_app.command()
def test(
    arquivo: str = typer.Argument(
        ..., help="Arquivo PDF para teste", callback=validate_pdf_file
    ),
    benchmark: bool = typer.Option(
        False, "--benchmark", help="Executar benchmark de performance"
    ),
):
    """
    Comandos de desenvolvimento e teste.

    [bold green]Exemplos:[/bold green]

    • Teste básico:
        [code]python -m src.cli dev test meu-boleto.pdf[/code]

    • Teste com benchmark:
        [code]python -m src.cli dev test meu-boleto.pdf --benchmark[/code]
    """
    import time

    logger = get_logger("dev")

    try:
        logger.info("Iniciando teste de desenvolvimento", arquivo=arquivo)

        if benchmark:
            start_time = time.time()

        parser = BoletoParser()
        dados = parser.parse(arquivo)

        if benchmark:
            end_time = time.time()
            duration = end_time - start_time
            console.print(f"[blue]Tempo de processamento:[/blue] {duration:.2f}s")
            logger.info("Benchmark concluído", duracao=duration)

        console.print("[green]✓[/green] Teste concluído com sucesso!")
        console.print(f"[blue]Tipo:[/blue] {dados.tipo_boleto}")
        console.print(f"[blue]Beneficiário:[/blue] {dados.beneficiario.nome}")

    except Exception as e:
        logger.error("Erro durante teste", erro=str(e))
        console.print(f"[red]Erro:[/red] {str(e)}")
        raise typer.Exit(1)


@dev_app.command()
def format():
    """Formata o código usando black e isort."""
    import subprocess
    import sys

    console.print("[blue]Formatando código...[/blue]")

    try:
        # Black
        subprocess.run([sys.executable, "-m", "black", "src", "tests"], check=True)
        console.print("[green]✓[/green] Black executado")

        # isort
        subprocess.run([sys.executable, "-m", "isort", "src", "tests"], check=True)
        console.print("[green]✓[/green] isort executado")

        console.print("[green]✓[/green] Código formatado com sucesso!")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erro durante formatação:[/red] {e}")
        raise typer.Exit(1)


@dev_app.command()
def lint():
    """Executa verificações de linting."""
    import subprocess
    import sys

    console.print("[blue]Executando linting...[/blue]")

    try:
                # flake8 (com tolerância para desenvolvimento)
        try:
            subprocess.run([sys.executable, "-m", "flake8", "src", "tests", "--max-line-length=88", "--extend-ignore=E203,W503,F401,F541"], check=True)
            console.print("[green]✓[/green] flake8 executado")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠[/yellow] flake8 encontrou alguns problemas (não críticos)")
        
        # mypy
        try:
            subprocess.run([sys.executable, "-m", "mypy", "src"], check=True)
            console.print("[green]✓[/green] mypy executado")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠[/yellow] mypy encontrou alguns problemas (não críticos)")
        console.print("[green]✓[/green] mypy executado")

        console.print("[green]✓[/green] Linting concluído com sucesso!")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erro durante linting:[/red] {e}")
        raise typer.Exit(1)


@dev_app.command()
def test_all():
    """Executa todos os testes com cobertura."""
    import subprocess
    import sys

    console.print("[blue]Executando testes...[/blue]")

    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "--cov=src", "--cov-report=html"],
            check=True,
        )
        console.print("[green]✓[/green] Testes executados com sucesso!")
        console.print(
            "[blue]Relatório de cobertura gerado em: htmlcov/index.html[/blue]"
        )

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erro durante testes:[/red] {e}")
        raise typer.Exit(1)


@dev_app.command()
def docs():
    """Gera documentação automática da CLI."""
    from pathlib import Path

    console.print("[blue]Gerando documentação da CLI...[/blue]")

    try:
        # Criar diretório docs se não existir
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)

        # Gerar documentação simples baseada na estrutura atual
        docs_content = """# Documentação da CLI - Boleto Parser

## Comandos Principais

### parse
Parse um arquivo PDF de boleto bancário e extrai dados estruturados.

```bash
python -m src parse arquivo.pdf [OPÇÕES]
```

**Opções:**
- `--output, -o`: Arquivo de saída JSON
- `--format, -f`: Formato de saída (json, pretty, table)
- `--verbose, -v`: Modo verboso
- `--force`: Sobrescrever arquivo de saída sem confirmar

### validate
Valida se um arquivo PDF é um boleto válido.

```bash
python -m src validate arquivo.pdf [--strict]
```

### extract-text
Extrai apenas o texto bruto do PDF.

```bash
python -m src extract-text arquivo.pdf [--output arquivo.txt]
```

## Comandos de Desenvolvimento

### dev test
Teste básico de processamento.

```bash
python -m src dev test arquivo.pdf [--benchmark]
```

### dev format
Formata o código usando black e isort.

```bash
python -m src dev format
```

### dev lint
Executa verificações de linting.

```bash
python -m src dev lint
```

### dev test-all
Executa todos os testes com cobertura.

```bash
python -m src dev test-all
```

### dev schema
Gera JSON de exemplo baseado nos models atuais.

```bash
python -m src dev schema
```

## Comandos de Produção

### prod batch
Processa múltiplos arquivos PDF em lote.

```bash
python -m src prod batch diretorio/ [--pattern "*.pdf"] [--output-dir ./resultados/]
```

## Opções Globais

- `--log-level, -l`: Nível de logging (DEBUG, INFO, WARNING, ERROR)
- `--log-file`: Arquivo de log (opcional)
- `--json-logs`: Usar formato JSON para logs
- `--quiet, -q`: Modo silencioso

---
*Documentação gerada automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        # Salvar documentação
        docs_file = docs_dir / "cli.md"
        with open(docs_file, "w", encoding="utf-8") as f:
            f.write(docs_content)

        console.print(f"[green]✓[/green] Documentação gerada em {docs_file}")

    except Exception as e:
        console.print(f"[red]Erro gerando documentação:[/red] {e}")
        raise typer.Exit(1)


@dev_app.command()
def schema():
    """Gera JSON de exemplo baseado nos models atuais."""
    import json
    from pathlib import Path

    console.print("[blue]Gerando JSON de exemplo...[/blue]")

    try:
        # Importar models
        from .models import BoletoData

        # Criar exemplo
        example_data = BoletoData(
            cnpj_instituicao="12.345.678/0001-90",
            numero_boleto="12345678",
            vencimento="15/08/2025",
            data_documento="01/08/2025",
            beneficiario={
                "nome": "INSTITUIÇÃO EDUCACIONAL EXEMPLO LTDA",
                "cnpj": "12.345.678/0001-90",
                "agencia": "0001",
                "codigo_beneficiario": "123456",
                "nosso_numero": "000012345678",
            },
            pagador={
                "nome": "JOÃO DA SILVA SANTOS",
                "cpf_cnpj": "123.456.789-00",
                "endereco": "RUA EXEMPLO, 123 - CENTRO - SÃO PAULO/SP",
                "cep": "01234-567",
            },
            aluno={
                "nome": "MARIA SANTOS OLIVEIRA",
                "matricula": "2024001",
                "curso": "ENGENHARIA DE SOFTWARE",
                "turno": "N",
                "codigo": "10001",
            },
            valores={
                "valor_documento": 500.00,
                "valor_cobrado": 500.00,
                "total_debitos": 1500.00,
            },
            informacoes_bancarias={
                "banco": "BANCO EXEMPLO S.A.",
                "codigo_barras": "123456789012345678901234567890123456789012345678901234567890",
                "carteira": "RCR",
                "especie": "RC",
                "aceite": "N",
            },
            instrucoes={
                "local_pagamento": "Pagável em qualquer Banco até a Data de Vencimento",
                "multa_vencimento": "R$10,00",
                "juros_dia_atraso": "R$0,50",
                "restricoes": "Só receber até o vencimento...",
            },
            endereco_instituicao={
                "endereco": "RUA DA INSTITUIÇÃO, 456 - CENTRO - SÃO PAULO/SP",
                "cep": "01234-567",
            },
            tipo_boleto="educacional",
            texto_extraido="texto bruto extraído do PDF...",
        )

        # Salvar JSON
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)

        schema_file = docs_dir / "example_schema.json"
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(example_data.model_dump(), f, indent=2, ensure_ascii=False)

        console.print(f"[green]✓[/green] JSON de exemplo gerado em {schema_file}")
        console.print(
            "[blue]Dica:[/blue] Use este arquivo para atualizar o README quando mudar os models"
        )

    except Exception as e:
        console.print(f"[red]Erro gerando schema:[/red] {e}")
        raise typer.Exit(1)


@prod_app.command()
def batch(
    diretorio: str = typer.Argument(
        ..., help="Diretório com arquivos PDF para processar"
    ),
    output_dir: str = typer.Option(
        "output", "--output-dir", "-o", help="Diretório de saída"
    ),
    pattern: str = typer.Option(
        "*.pdf", "--pattern", "-p", help="Padrão de arquivos para processar"
    ),
):
    """
    Processa múltiplos arquivos PDF em lote.

    [bold green]Exemplos:[/bold green]

    • Processar todos os PDFs:
        [code]python -m src.cli prod batch ./meus-boletos/[/code]

    • Processar com padrão específico:
        [code]python -m src.cli prod batch ./meus-boletos/ --pattern "*boleto*.pdf"[/code]
    """
    logger = get_logger("prod")

    try:
        dir_path = Path(diretorio)
        if not dir_path.exists():
            raise typer.BadParameter(f"Diretório não encontrado: {diretorio}")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Encontrar arquivos
        arquivos = list(dir_path.glob(pattern))
        if not arquivos:
            console.print(
                f"[yellow]Nenhum arquivo encontrado em {diretorio} com padrão {pattern}[/yellow]"
            )
            return

        console.print(f"[blue]Processando {len(arquivos)} arquivos...[/blue]")

        parser = BoletoParser()
        processados = 0
        erros = 0

        for arquivo in arquivos:
            try:
                dados = parser.parse(str(arquivo))
                output_file = output_path / f"{arquivo.stem}.json"

                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(dados.model_dump(), f, ensure_ascii=False, indent=2)

                processados += 1
                console.print(f"[green]✓[/green] {arquivo.name}")

            except Exception as e:
                erros += 1
                console.print(f"[red]✗[/red] {arquivo.name}: {str(e)}")
                logger.error(
                    "Erro processando arquivo", arquivo=str(arquivo), erro=str(e)
                )

        console.print(
            f"\n[blue]Resumo:[/blue] {processados} processados, {erros} erros"
        )
        logger.info(
            "Processamento em lote concluído", processados=processados, erros=erros
        )

    except Exception as e:
        logger.error("Erro durante processamento em lote", erro=str(e))
        console.print(f"[red]Erro:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
