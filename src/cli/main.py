import typer

from .dev import dev_app
from .prod import prod_app

app = typer.Typer(
    help="Parser inteligente de boletos bancários PDF",
    add_completion=False,
    rich_markup_mode="rich",
)

# Registrar subcomandos
app.add_typer(dev_app, name="dev")
app.add_typer(prod_app, name="prod")
