from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    KEY: str = ""
    ALGORITHM: str = ""

    HEMIS_GET_EMPLOYEES: str = ""
    HEMIS_GET_STUDENTS: str = ""
    HEMIS_GET_STUDENT: str = ""
    HEMIS_TOKEN: str = ""

    USER_URL: str = "uploads/users/"
    DOCUMENT_URL: str = "uploads/documents/"

    model_config = SettingsConfigDict(env_file="../.env")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()


print(f"{settings=}")
