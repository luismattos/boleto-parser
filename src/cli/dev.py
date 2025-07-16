import sys

import typer
from rich.console import Console

from .helpers import run_subprocess

# Sub-app de desenvolvimento
dev_app = typer.Typer(help="Comandos de desenvolvimento e debug")
console = Console()


@dev_app.command()
def test_all():
    """Executa todos os testes com cobertura via Nox."""
    console.print("[blue]Executando todos os testes via Nox...[/blue]")
    try:
        run_subprocess([sys.executable, "-m", "nox", "--version"], check=True)
    except Exception:
        console.print("[red]✗[/red] Nox não está instalado")
        console.print("[blue]Dica:[/blue] Execute 'poetry install --with dev'")
        raise typer.Exit(1)
    result = run_subprocess([sys.executable, "-m", "nox", "-s", "tests"])
    if result.returncode == 0:
        console.print("[green]✓[/green] Testes executados com sucesso via Nox!")
    else:
        raise typer.Exit(result.returncode)
