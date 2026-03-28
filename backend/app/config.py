from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase (new key format: sb_publishable_* / sb_secret_*)
    SUPABASE_URL: str
    NEXT_PUBLIC_SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    @property
    def SUPABASE_ANON_KEY(self) -> str:
        return self.NEXT_PUBLIC_SUPABASE_ANON_KEY

    # LLM
    LLM_PROVIDER: str = "openrouter"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct:free"

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = "us-east-1"
    BEDROCK_PRIMARY_MODEL: str = "meta.llama3-3-70b-instruct-v1:0"
    BEDROCK_FALLBACK_MODEL: str = "anthropic.claude-sonnet-4-20250514-v1:0"

    # Model / S3
    MODEL_SOURCE: str = "s3"  # "s3" or "local"
    S3_BUCKET: str = "shifamind-models"
    S3_MODEL_KEY: str = "phase1/phase1_best.pt"
    S3_THRESHOLDS_KEY: str = "phase1/optimal_thresholds.json"
    LOCAL_MODEL_PATH: str = "model/phase1_best.pt"
    LOCAL_THRESHOLDS_PATH: str = "model/optimal_thresholds.json"
    DEVICE: str = "cpu"

    # App
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "https://platform.shifamind.me,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
