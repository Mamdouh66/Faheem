import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics


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
