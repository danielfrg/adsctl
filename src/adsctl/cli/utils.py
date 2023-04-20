import sys
from typing import Optional

import click

from adsctl.application import Application
from adsctl.config.config_file import ConfigFile
from adsctl.utils.fs import Path


def create_app(
    config_file_path: Optional[str] = None, customer_id: Optional[str] = None
) -> Application:
    used_config_file = Path()

    app = Application(
        config_file=ConfigFile(),
        customer_id=customer_id,
        load_config=False,
        create_client=False,
    )

    if config_file_path:
        used_config_file = Path(config_file_path).resolve()
        if not used_config_file.is_file():
            click.echo(
                f"The selected config file `{str(config_file_path)}` does not exist."
            )
            sys.exit(1)
        app.config_file = ConfigFile(used_config_file)

    return app


def replace_field(content: str, field: str, prev_value: str, new_value: str) -> str:
    new_content = content

    field_line = f'{field} = "{prev_value}"'

    occurrences = content.count(field_line)

    if occurrences == 1:
        new_line = f'{field} = "{new_value}"'
        new_content = new_content.replace(field_line, new_line)

    return new_content
