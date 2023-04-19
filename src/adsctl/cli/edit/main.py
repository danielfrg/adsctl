import click

from .campaign import campaign


@click.group()
def edit():
    pass


edit.add_command(campaign)
