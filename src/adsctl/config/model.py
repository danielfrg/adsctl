from pydantic import (
    BaseModel,
    BaseSettings,
)


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
