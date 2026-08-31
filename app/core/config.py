from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    SUPABASE_JWT_KID: str
    SUPABASE_JWT_X: str
    SUPABASE_JWT_Y: str

    HF_TOKEN:str

    FE_URL:str

    class Config:
        env_file = ".env"


settings = Settings()