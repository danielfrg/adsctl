import re

from pydantic import BaseModel, BaseSettings, validator


class OAuth(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str | None = None


class AccountConfig(BaseModel):
    developer_token: str = ""
    customer_id: str = ""
    login_customer_id: str = ""
    oauth: OAuth = OAuth()

    @validator("customer_id", "login_customer_id")
    def valid_customer_id(cls, value, **kwargs):
        if not re.match("^[0-9-]*$", value):
            raise ValueError("Only numbers and dashes allowed in customer_id")
        return value.replace("-", "")

    def clientSettings(self):
        base = {
            "developer_token": self.developer_token,
            "client_id": self.oauth.client_id,
            "client_secret": self.oauth.client_secret,
            "refresh_token": self.oauth.refresh_token,
            "use_proto_plus": False,
        }

        if self.login_customer_id:
            base["login_customer_id"] = self.login_customer_id
        return base


class RootConfig(BaseSettings):
    current_account: str = "default"
    accounts: dict[str, AccountConfig] = {
        "default": AccountConfig(),
    }

    class Config:
        env_prefix = "adsctl_"
