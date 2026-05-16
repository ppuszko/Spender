from pydantic_settings import BaseSettings, SettingsConfigDict


class MailSettings(BaseSettings): 
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int 

    MAIL_FROM_NAME: str = "Spender"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True  


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

MailConfig = MailSettings() # type: ignore