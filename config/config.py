from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env.dev"
        orm_mode = True