"""
Application configuration management using Pydantic Settings.

This module defines the centralized configuration for the License Classificator
service, supporting multiple deployment environments (local, Docker, cloud) and
LLM provider abstractions (Ollama, OpenAI).

Configuration values are loaded from:
1. Environment variables (highest priority)
2. .env file (if present)
3. Default values defined in the Settings class

The configuration is accessed globally via the [`settings`](app/core/config.py)
singleton instance.

Example:
    >>> from app.core.config import settings
    >>> settings.llm_provider
    'ollama'
    >>> settings.sqlite_path
    'app.db'

Environment Variables:
    INPUT_XLSX_PATH: Path to input Excel file (default: "licenses.xlsx")
    OUTPUT_DIR: Directory for output files (default: "output")
    OUTPUT_XLSX_PATH: Path to output Excel file (default: "output/output.xlsx")
    SQLITE_PATH: SQLite database file path (default: "app.db")
    LLM_PROVIDER: LLM backend ("ollama" or "openai", default: "ollama")
    OLLAMA_BASE_URL: Ollama API endpoint (default: "http://host.docker.internal:11434")
    OLLAMA_MODEL: Ollama model name (default: "llama3.1:8b")
    OPENAI_API_KEY: OpenAI API key (required if LLM_PROVIDER="openai")
    OPENAI_MODEL: OpenAI model name (default: "gpt-4o-mini")

Note:
    The [`ollama_base_url`](app/core/config.py) defaults to `host.docker.internal:11434`
    for Docker deployments. For local development, change to `http://localhost:11434`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration schema using Pydantic Settings.

    Defines all configurable parameters for the License Classificator service,
    including I/O paths, database settings, and LLM provider configuration.
    Values are automatically populated from environment variables or .env file.

    Attributes:
        input_xlsx_path: Path to input Excel file containing licenses
        output_dir: Directory where classification results are saved
        output_xlsx_path: Full path to output Excel file with classifications
        sqlite_path: Path to SQLite database file for persistence
        llm_provider: LLM backend selection ("ollama" or "openai")
        ollama_base_url: Base URL for Ollama API endpoint
        ollama_model: Model name for Ollama inference
        openai_api_key: API key for OpenAI (None if not using OpenAI)
        openai_model: Model name for OpenAI inference
        model_config: Pydantic settings configuration (loads from .env)

    Example:
        >>> settings = Settings()
        >>> settings.llm_provider
        'ollama'
        >>> settings.input_xlsx_path
        'licenses.xlsx'

    Note:
        This class is instantiated once as the global [`settings`](app/core/config.py)
        instance. Use that singleton instead of creating new instances.
    """

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
