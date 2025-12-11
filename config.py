from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mongo_uri: str = Field("mongodb://localhost:27017", env="MONGO_URI")
    master_db_name: str = Field("multi_tenant_master", env="MASTER_DB_NAME")
    jwt_secret_key: str = Field("super-secret-change-me", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_exp_minutes: int = Field(60, env="JWT_EXP_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

