import pickle

import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB


def plot_confusion_matrix(y_test: np.ndarray, y_pred: np.ndarray, labels: list) -> None:
    """
    Plots the confusion matrix based on the predicted and true labels for mlflow tracking.

    Args:
        y_test (np.ndarray): The true labels.
        y_pred (np.ndarray): The predicted labels.
        labels (list): The list of class labels.

    Returns:
        None
    """
    cm = metrics.confusion_matrix(y_test, y_pred, labels=labels)
    disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.savefig("notebooks/dump/confusion_matrix.png")
    plt.close()


def load_model(path: str) -> MultinomialNB:
    """
    Load a model from the provided path.

    Args:
        path (str): The path to the model file.

    Returns:
        object: The loaded model.
    """
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model
