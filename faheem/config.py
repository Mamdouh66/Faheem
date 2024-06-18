import os
import sys
import logging

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

    LOGS_DIR: str = str(Path().resolve()) + str(Path("/logs").absolute())


settings = Settings()

if not os.path.exists(settings.LOGS_DIR):
    print("Creating logs directory...")
    os.makedirs(settings.LOGS_DIR)

logging_config: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(settings.LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(settings.LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["console", "info", "error"],
        "level": logging.INFO,
        "propagate": True,
    },
}
logging.config.dictConfig(logging_config)
logger = logging.getLogger()
