import typer
from .wrapper.ngspice import ng_spice

"""could be :
    from importlib import import_module
    module = import_module(var: str)
"""
cli = typer.Typer()
cli.add_typer(ng_spice, name="ngspice")


if __name__ == "__main__":
    cli()
