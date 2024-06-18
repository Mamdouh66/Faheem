import os

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MLFLOW_TRACKING_URI: str = Field(
        default=str(Path().resolve()) + str(Path("/tmp/mlflow").absolute()),
        description="URI of the MLflow tracking server.",
    )
    PATH_TO_DATA: dict = Field(
        default={
            "test_arabic_negative_tweets": "data/test_arabic_negative_tweets.tsv",
            "test_arabic_positive_tweets": "data/test_arabic_positive_tweets.tsv",
            "train_arabic_negative_tweets": "data/train_arabic_negative_tweets.tsv",
            "train_arabic_positive_tweets": "data/train_arabic_positive_tweets.tsv",
        },
        description="Path to the Arabic data, which is used to train the model.",
    )
    PATH_TO_MODEL: str = Field(
        default="notebooks/models/nb_model.pkl",
        description="Path to the trained model, which is used to predict the sentiment of the Arabic text.",
    )

    LOGS_DIR: str = Field(
        default=str(Path().resolve()) + str(Path("/logs").absolute()),
        description="Directory to store the logs.",
    )


settings = Settings()

if not os.path.exists(settings.LOGS_DIR):
    print("Creating logs directory...")
    os.makedirs(settings.LOGS_DIR)
