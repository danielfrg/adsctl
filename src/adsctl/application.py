from typing import Optional

from google.ads.googleads.client import GoogleAdsClient

from adsctl import client
from adsctl.config.config_file import ConfigFile
from adsctl.config.model import AccountConfig, RootConfig
from adsctl.parse import parseStream


class Application:
    config_file: ConfigFile
    client: GoogleAdsClient | None
    _customer_id: Optional[str]
    params: dict = {}

    def __init__(
        self, config_file=None, customer_id=None, load_config=True, create_client=True
    ):
        self.config_file = config_file or ConfigFile()
        self._customer_id = customer_id

        if load_config:
            self.load_config()

        self.client = None
        if create_client:
            self.create_client()

    @property
    def config(self) -> RootConfig:
        return self.config_file.model

    @property
    def customer_id(self) -> str | None:
        if self._customer_id is not None:
            return self._customer_id.replace("-", "")

    @property
    def account(self) -> AccountConfig:
        return self.config_file.account

    @customer_id.setter
    def customer_id_set(self, value: str | None):
        if value is not None:
            self._customer_id = value

    def load_config(self):
        self.config_file.load()

        # Use default from __init__ or config file
        self._customer_id = self._customer_id or self.config_file.account.customer_id

    def create_client(self):
        if self.client is None:
            gads_config = self.config_file.account.clientSettings()
            self.client = client.get_client(gads_config)

    def search(self, query, customer_id=None):
        customer_id = customer_id or self.config_file.account.customer_id
        stream = client.search(query.strip(), self.client, customer_id)
        return stream

    def search_stream(self, query, customer_id=None):
        customer_id = customer_id or self.config_file.account.customer_id
        stream = client.search_stream(query.strip(), self.client, customer_id)
        return stream

    def query(self, query, customer_id=None):
        stream = self.search_stream(query, customer_id=customer_id)
        tables = parseStream(stream)
        return tables


# Alias
GoogleAds = Application
GoogleAds = Application
