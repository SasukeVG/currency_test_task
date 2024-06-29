from pydantic_settings import BaseSettings, SettingsConfigDict


class SGIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CURRENCY_ENV_')

    HTTP_PROTOCOL: str = "http"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    WORKERS_COUNT: int = 1

    AUTO_RELOAD: bool = True
    TIMEOUT: int = 60

    WSGI_APP: str = "web_app.api.main:app"
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"


sgi_config = SGIConfig()