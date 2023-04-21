import sys

import click

from adsctl.application import Application
from adsctl.utils.fs import Path


def create_app(
    config_file_path: str | None = None,
    customer_id: str | None = None,
    account: str | None = None,
) -> Application:

    if config_file_path:
        used_config_file = Path(config_file_path).resolve()
        if not used_config_file.is_file():
            click.echo(
                f"The selected config file `{str(config_file_path)}` does not exist."
            )
            sys.exit(1)

    app = Application(
        config_file=config_file_path,
        customer_id=customer_id,
        account=account,
        load_config=False,
    )

    return app


def replace_field(content: str, field: str, prev_value: str, new_value: str) -> str:
    new_content = content

    field_line = f'{field} = "{prev_value}"'

    occurrences = content.count(field_line)

    if occurrences == 1:
        new_line = f'{field} = "{new_value}"'
        new_content = new_content.replace(field_line, new_line)

    return new_content
