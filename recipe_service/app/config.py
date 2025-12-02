from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    app_name: str = "Recipe Service"
    default_page_size: int = 20
    feature_preview: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",      
        env_prefix="RECIPE_", 
        extra="ignore",
    )
