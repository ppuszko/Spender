from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    JWT_SECRET: str
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

AuthConfig = Settings() # type: ignore