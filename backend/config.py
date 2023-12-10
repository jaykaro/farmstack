from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Starter"
    DEBUG_MODE: bool = False

class ServerSettings(BaseSettings):
    Host: STR = "0.0.0.0"