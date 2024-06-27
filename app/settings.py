import os
from pathlib import Path
from datetime import date, datetime

from pydantic import BaseModel, model_validator

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

CURRENT_DATE = date.today()
CURRENT_TIME = datetime.now().time()

load_dotenv(BASE_DIR / ".env")


class BaseEnv(BaseModel):
    service_domain: str = os.environ.get("SERVICE_DOMAIN")


class DbCreds(BaseModel):
    database: str = os.environ.get("SQL_DATABASE")
    user: str = os.environ.get("SQL_USER")
    password: str = os.environ.get("SQL_PASSWORD")
    host: str = os.environ.get("SQL_HOST", "localhost")
    port: int = int(os.environ.get("SQL_PORT", 5432))
    database_url: str | None = os.environ.get("DATABASE_URL")

    @model_validator(mode="after")
    def model_validations(self):
        if not self.database_url:
            self.database_url = (f"postgresql+"
                                 f"psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        return self
