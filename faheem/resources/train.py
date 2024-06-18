import time
import json

import numpy as np
import polars as pl
import mlflow

from typing import Tuple

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from faheem.resources.utils import plot_confusion_matrix
from faheem.config import settings, logger
from faheem.resources.evaluate import get_overall_metrics, get_per_class_metrics


def get_numpy_X_y(df: pl.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the numpy arrays for X ('clean_tweet') and y ('labels') data from a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame containing the data.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing the numpy arrays for X and y.
    """
    X = df["cleaned_tweet"].to_numpy()
    y = df["label"].to_numpy()

    return X, y


def split_data(
    X: np.ndarray, y: np.ndarray, test_size: float = 0.2, shuffle: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split the data into training and testing sets.

    Args:
        `X` (np.ndarray): The input features.
        `y` (np.ndarray): The target labels.
        `test_size` (float, optional): The proportion of the data to include in the test set. `Defaults to 0.2`.
        `shuffle` (bool, optional): Whether to shuffle the data before splitting. `Defaults to True`.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: A tuple containing the training and testing sets for X and y.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, shuffle=shuffle
    )
    return X_train, X_test, y_train, y_test


def train_model(
    df: pl.DataFrame, experiment_name: str = "MultinomialNB Experiment"
) -> MultinomialNB:
    """
    Train a Multinomial Naive Bayes model on the provided DataFrame, log the experiment with MLflow,
    and save the confusion matrix plot.

    Args:
        df (pl.DataFrame): A Polars DataFrame containing the features and labels for training.
        experiment_name (str): The name of the MLflow experiment. Default is "MultinomialNB Experiment".

    Returns:
        model (MultinomialNB): The trained Multinomial Naive Bayes model.
    """
    X, y = get_numpy_X_y(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    logger.info("Training the Multinomial Naive Bayes model...")
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(experiment_name=experiment_name)
    with mlflow.start_run():
        mlflow.log_param("model_type", "MultinomialNB")

        model = MultinomialNB()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = metrics.accuracy_score(y_test, y_pred)
        report = metrics.classification_report(y_test, y_pred, output_dict=True)
        mlflow.log_metric("accuracy", accuracy)
        for label, metrics_dict in report.items():
            if isinstance(metrics_dict, dict):
                for metric_name, metric_value in metrics_dict.items():
                    mlflow.log_metric(f"{label}_{metric_name}", metric_value)

        mlflow.sklearn.log_model(model, "model")
        log_d = {
            "run_id": mlflow.active_run().info.run_id,
            "experiment_id": mlflow.active_run().info.experiment_id,
            "overall_metrics": get_overall_metrics(y_test, y_pred),
            "per_class_metrics": get_per_class_metrics(y_test, y_pred),
        }
        logger.info(f"Logging the run details: {json.dumps(log_d, indent=2)}")

        unique_labels = list(set(y_test))
        plot_confusion_matrix(y_test, y_pred, labels=unique_labels)
        mlflow.log_artifact("./dump/confusion_matrix.png")

    return model
