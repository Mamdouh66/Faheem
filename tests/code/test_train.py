import pytest

import numpy as np

from faheem.resources.train import split_data


def test_split_data():
    X = np.arange(100).reshape((50, 2))
    y = np.array([0, 1] * 25)

    X_train, X_test, y_train, y_test = split_data(X, y)

    assert X_train.shape[0] == 40
    assert X_test.shape[0] == 10
    assert y_train.shape[0] == 40
    assert y_test.shape[0] == 10

    # Check if the proportion of classes in y_train and y_test are same as in y
    assert np.allclose(
        np.bincount(y) / len(y), np.bincount(y_train) / len(y_train), atol=0.1
    )
    assert np.allclose(
        np.bincount(y) / len(y), np.bincount(y_test) / len(y_test), atol=0.1
    )

    # Test without shuffling
    X_train_ns, X_test_ns, y_train_ns, y_test_ns = split_data(X, y, shuffle=False)

    # Check that the data is not shuffled
    assert np.array_equal(X[:40], X_train_ns)
    assert np.array_equal(X[40:], X_test_ns)
    assert np.array_equal(y[:40], y_train_ns)
    assert np.array_equal(y[40:], y_test_ns)

    # Test with a different test_size
    X_train_small, X_test_small, y_train_small, y_test_small = split_data(
        X, y, test_size=0.1
    )

    # Check the size of the splits
    assert X_train_small.shape[0] == 45
    assert X_test_small.shape[0] == 5
    assert y_train_small.shape[0] == 45
    assert y_test_small.shape[0] == 5
