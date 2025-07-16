import subprocess

from rich.console import Console

console = Console()


def run_subprocess(cmd, **kwargs):
    """Executa um comando subprocesso e exibe saída formatada."""
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.stdout:
        console.print(result.stdout)
    if result.stderr:
        console.print(result.stderr)
    return result
