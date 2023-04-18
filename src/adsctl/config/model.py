from pydantic import BaseModel, BaseSettings


class OAuth(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str = ""


class RootConfig(BaseSettings):
    developer_token: str = ""
    customer_id: str = ""
    login_customer_id: str = ""
    oauth: OAuth = OAuth()

    class Config:
        env_prefix = "adsctl_"

    def clientSettings(self):
        return {
            "developer_token": self.developer_token,
            "login_customer_id": self.login_customer_id,
            "client_id": self.oauth.client_id,
            "client_secret": self.oauth.client_secret,
            "refresh_token": self.oauth.refresh_token,
            "use_proto_plus": False,
        }
