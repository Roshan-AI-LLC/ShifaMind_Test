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
    OPENROUTER_MODEL: str = "google/gemma-4-26b-a4b-it:free"

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = "us-east-1"
    BEDROCK_PRIMARY_MODEL: str = "meta.llama3-3-70b-instruct-v1:0"
    BEDROCK_FALLBACK_MODEL: str = "anthropic.claude-sonnet-4-20250514-v1:0"

    # Model artifacts
    MODEL_SOURCE: str = "s3"  # "s3" or "local"
    S3_BUCKET: str = "shifamind-models"
    S3_FULLCODE_MODEL_KEY: str = "models/fullcode/s10/model.pt"
    S3_FULLCODE_THRESHOLDS_KEY: str = "models/fullcode/s10/thresholds.json"
    S3_FULLCODE_LABELS_KEY: str = "models/fullcode/s10/label_vocab.json"
    S3_FULLCODE_BANK_KEY: str = "models/fullcode/s10/concept_bank.jsonl"
    S3_FULLCODE_TITLES_KEY: str = "models/fullcode/s10/code_titles.json"
    LOCAL_FULLCODE_DIR: str = "artifacts/fullcode"
    # Mounted as a docker volume so the 758 MB checkpoint survives `docker rm`
    # and an instance stop/start, and is pulled once rather than every boot.
    FULLCODE_CACHE_DIR: str = "/var/lib/shifamind/fullcode"
    # 0 means use the validation-selected micro threshold from thresholds.json.
    THRESHOLD: float = 0
    DEVICE: str = "cpu"

    # App
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = "https://platform.roshan-ai.com,https://platform.shifamind.me,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
