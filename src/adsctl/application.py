from typing import Optional

from google.ads.googleads.client import GoogleAdsClient

from adsctl import client as client_utils
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
    def account(self) -> AccountConfig:
        return self.config_file.account

    @property
    def customer_id(self) -> str | None:
        if self._customer_id is not None:
            return self._customer_id.replace("-", "")

    @customer_id.setter
    def customer_id_set(self, value: str):
        if value is not None:
            self._customer_id = value

    def load_config(self):
        self.config_file.load()

        # Use default from __init__ or config file
        self._customer_id = self._customer_id or self.config_file.account.customer_id

    def create_client(self):
        gads_config = self.config_file.account.clientSettings()
        client_ = client_utils.get_client(gads_config)
        self.client = client_
        return client_

    def query(self, query, customer_id=None, params: dict | None = None):
        if params is None:
            params = {}
        customer_id = customer_id or self.config_file.account.customer_id
        myclient = self.create_client()
        stream = self.search_stream(query=query, client=myclient, params=params)
        tables = parseStream(stream)
        return tables

    def search(self, query, client, customer_id=None, params: dict | None = None):
        if params is None:
            params = {}
        customer_id = customer_id or self.customer_id
        query_ = client_utils.render_template(query.strip(), **params)

        ga_service = client.get_service("GoogleAdsService")
        return ga_service.search(query=query_, customer_id=customer_id)

    def search_stream(
        self, query, client, customer_id=None, params: dict | None = None
    ):
        if params is None:
            params = {}
        customer_id = customer_id or self.customer_id
        query_ = client_utils.render_template(query.strip(), **params)
        print(query_)

        ga_service = client.get_service("GoogleAdsService")
        return ga_service.search_stream(query=query_, customer_id=customer_id)


# Alias
GoogleAds = Application
