from pydantic import (AmqpDsn, BaseModel, BaseSettings, Field, PostgresDsn,
                      PyObject, RedisDsn)


def parse_config(obj):
    if isinstance(obj, LazilyParsedConfig):
        obj.parse_fields()
    elif isinstance(obj, list):
        for o in obj:
            parse_config(o)
    elif isinstance(obj, dict):
        for o in obj.values():
            parse_config(o)


class LazilyParsedConfig:
    def __init__(self, config: dict, steps: tuple = ()):
        self.raw_data = config
        self.steps = steps

    def parse_fields(self):
        for attribute in self.__dict__:
            _, prefix, name = attribute.partition('_field_')
            if prefix:
                parse_config(getattr(self, name))

    # def raise_error(self, message, *, extra_steps=()):
    #     import inspect

    #     field = inspect.currentframe().f_back.f_code.co_name
    #     raise Exception(message)
    #     # raise ConfigurationError(message, location=' -> '.join([*self.steps, field, *extra_steps]))



class OAuth(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str = ""


class RootConfig(BaseSettings, LazilyParsedConfig):
    developer_token: str = ""
    customer_id: str = ""
    login_customer_id: str = ""
    oauth: OAuth = OAuth()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Config:
        env_prefix = 'adsctl_'
