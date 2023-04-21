from typing import cast

from adsctl.config.model import AccountConfig, RootConfig
from adsctl.utils.fs import Path, load_toml_data


class ConfigFile:
    model: RootConfig
    account_name: str | None

    def __init__(self, path: Path | None = None, account: str | None = None):
        self._path: Path | None = path
        self.model = cast(RootConfig, None)
        self.account_name = account

    @property
    def path(self):
        if self._path is None:
            self._path = self.get_default_location()
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def account(self) -> AccountConfig:
        """Return the Current Account Model"""
        return self.model.accounts[self.account_name or self.model.current_account]

    def save(self, content=None):
        import tomli_w

        if not content:
            content = tomli_w.dumps(self.model.dict(exclude_none=True))

        self.path.ensure_parent_dir_exists()
        self.path.write_atomic(content, "w", encoding="utf-8")

    def load(self):
        self.model = RootConfig.parse_obj(load_toml_data(self.read()))

    def read(self) -> str:
        return self.path.read_text("utf-8")

    def restore(self):
        import tomli_w

        config = RootConfig()

        content = tomli_w.dumps(config.dict(exclude_none=True))
        self.save(content)

        self.model = config

    def update(self):
        self.save()

    @classmethod
    def get_default_location(cls) -> Path:
        from platformdirs import user_config_dir

        return Path(user_config_dir("adsctl", appauthor=False)) / "config.toml"
