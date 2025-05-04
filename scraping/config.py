from pydantic_settings import BaseSettings, SettingsConfigDict

class ScraperSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    LINKEDIN_USER: str
    LINKEDIN_PASS: str
    SCRAPE_DELAY: float = 5.0

    SCROLLS: int = 5
    JOB_LIMIT: int = 50
    SCROLL_DELAY: float = 2.0

    PAGE_LOAD_TIMEOUT: int = 20
    APPLICANT_RETRIES: int = 2
    APPLICANT_DELAY: float = 2.0

settings = ScraperSettings()