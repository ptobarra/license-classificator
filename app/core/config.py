from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Input/Output
    input_xlsx_path: str = "licenses.xlsx"
    output_dir: str = "output"
    output_xlsx_path: str = "output/output.xlsx"

    # DB
    sqlite_path: str = "app.db"

    # LLM provider: "ollama" or "openai"
    llm_provider: str = "ollama"

    # Ollama
    # ollama_base_url: str = "http://localhost:11434"  # For local use
    ollama_base_url: str = "http://host.docker.internal:11434"  # For Docker use
    ollama_model: str = "llama3.1:8b"

    # OpenAI (optional)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    # class Config:
    #     env_file = ".env"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
