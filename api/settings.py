from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # AUTH
    secret_key: str

    sqladmin_password: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
