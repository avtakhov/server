from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # AUTH
    secret_key: str
    algorithm: str = "HS256"

    sqladmin_password: str
    api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
