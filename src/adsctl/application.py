from typing import Union

from google.ads.googleads.client import GoogleAdsClient

from adsctl import client as client_utils
from adsctl.config.config_file import ConfigFile
from adsctl.config.model import AccountConfig, RootConfig
from adsctl.parse import parseStream
from adsctl.utils.fs import Path


class Application:
    config_file_path: Union[Path, None]
    config_file: ConfigFile
    client: Union[GoogleAdsClient, None]
    _customer_id: Union[str, None]
    params: dict = {}
    api_version: str = "v13"

    def __init__(
        self,
        config_file: Union[str, None] = None,  # Path to config file
        account: Union[str, None] = None,
        customer_id: Union[str, None] = None,
        load_config=True,
    ):
        self._customer_id = customer_id
        if config_file is None:
            self.config_file_path = ConfigFile.get_default_location()
            self.config_file = ConfigFile(account=account)
        else:
            self.config_file_path = Path(config_file)
            path_ = None if config_file is None else Path(config_file)
            self.config_file = ConfigFile(path=path_, account=account)

        if load_config:
            self.load_config()

    @property
    def config(self) -> RootConfig:
        return self.config_file.model

    @property
    def account(self) -> AccountConfig:
        return self.config_file.account

    @property
    def customer_id(self) -> Union[str, None]:
        if self._customer_id:
            return self._customer_id.replace("-", "")
        else:
            return self.account.customer_id.replace("-", "")

    def load_config(self):
        self.config_file.load()

    def create_client(self):
        gads_config = self.config_file.account.clientSettings()
        client_ = client_utils.get_client(gads_config, version=self.api_version)
        self.client = client_
        return client_

    def query(
        self, query, customer_id=None, params: Union[dict, None] = None, **kwargs
    ):
        if params is None:
            params = {}
        customer_id = customer_id or self.config_file.account.customer_id

        results = self.search_stream(query=query, params=params, **kwargs)

        tables = parseStream(results)
        return tables

    def search(
        self, query, customer_id=None, params: Union[dict, None] = None, **kwargs
    ):
        if params is None:
            params = {}
        customer_id = customer_id or self.customer_id or self.account.customer_id
        query_ = client_utils.render_template(query.strip(), **params)

        myclient = self.create_client()
        ga_service = myclient.get_service("GoogleAdsService")

        request = kwargs or {}
        request["query"] = query_
        request["customer_id"] = customer_id

        results = ga_service.search(request=request)
        rows = []
        for row in results:
            rows.append(row)

        if results.summary_row:
            rows.append(results.summary_row)

        return rows

    def search_stream(
        self, query, customer_id=None, params: Union[dict, None] = None, **kwargs
    ):
        if params is None:
            params = {}
        customer_id = customer_id or self.customer_id or self.account.customer_id
        query_ = client_utils.render_template(query.strip(), **params)

        myclient = self.create_client()
        ga_service = myclient.get_service("GoogleAdsService")

        request = kwargs or {}
        request["query"] = query_
        request["customer_id"] = customer_id

        stream = ga_service.search_stream(request=request)

        rows = []
        for batch in stream:
            for row in batch.results:
                rows.append(row)

            if batch.summary_row:
                rows.append(batch.summary_row)

        return rows


# Alias
GoogleAds = Application
