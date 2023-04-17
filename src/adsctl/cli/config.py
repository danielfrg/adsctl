import click


@click.group()
@click.pass_obj
def config(app):
    """View and manage configuration"""


@config.command()
@click.pass_obj
def info(app):
    """Show information about the config."""
    click.echo(f"Config file: {app.config_file.path}")


@config.command()
@click.pass_obj
def explore(app):
    """Open the config location in your file manager."""
    click.launch(str(app.config_file.path), locate=True)


@config.command()
@click.pass_obj
def show(app):
    """Show the contents of the config file."""
    if not app.config_file.path.is_file():  # no cov
        app.display_critical("No config file found! Try: `adsctl config restore`.")
    else:
        click.echo(app.config_file.read())
