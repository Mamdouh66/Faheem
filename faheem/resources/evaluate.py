import numpy as np

from typing import OrderedDict

from sklearn import metrics


def get_overall_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Calculate the overall metrics.

    Args:
        `y_true` (np.ndarray): The true labels.
        `y_pred` (np.ndarray): The predicted labels.

    Returns:
        overall_metrics (dict): containing the overall metrics:\n
            - `precision`: The precision score.
            - `recall`: The recall score.
            - `f1`: The F1 score.
            - `num_samples`: The number of samples.

    """
    evals = metrics.precision_recall_fscore_support(y_true, y_pred, average="weighted")
    overall_metrics = {
        "precision": evals[0],
        "recall": evals[1],
        "f1": evals[2],
        "num_samples": np.float64(len(y_true)),
    }
    return overall_metrics


def get_per_class_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, class_to_index: dict
) -> dict:
    """
    Calculate per-class metrics for a multi-class classification problem.

    Args:
        y_true (np.ndarray): True labels of the samples.
        y_pred (np.ndarray): Predicted labels of the samples.
        class_to_index (dict): Mapping of class names to their corresponding indices.

    Returns:
        dict: A dictionary containing per-class metrics, including precision, recall, F1-score,
              and the number of samples for each class. The dictionary is sorted in descending
              order based on the F1-score.

    """
    per_class_metrics = {}
    evals = metrics.precision_recall_fscore_support(y_true, y_pred, average=None)
    for i, _class in enumerate(class_to_index):
        per_class_metrics[_class] = {
            "precision": evals[0][i],
            "recall": evals[1][i],
            "f1": evals[2][i],
            "num_samples": np.float64(evals[3][i]),
        }
    sorted_per_class_metrics = OrderedDict(
        sorted(per_class_metrics.items(), key=lambda tag: tag[1]["f1"], reverse=True)
    )
    return sorted_per_class_metrics
