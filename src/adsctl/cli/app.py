from typing import Optional

from adsctl.config.config_file import ConfigFile


class Application:
    def __init__(self, config_file):
        self.config_file: ConfigFile = config_file
        self.client = None
        self.customer_id: Optional[str]
