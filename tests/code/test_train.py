import pytest

import numpy as np

from faheem.resources.data import get_clean_data
from faheem.resources.train import split_data, train_model, get_numpy_X_y

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


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

    assert np.array_equal(X[:40], X_train_ns)
    assert np.array_equal(X[40:], X_test_ns)
    assert np.array_equal(y[:40], y_train_ns)
    assert np.array_equal(y[40:], y_test_ns)

    # Test with a different test_size
    X_train_small, X_test_small, y_train_small, y_test_small = split_data(
        X, y, test_size=0.1
    )

    assert X_train_small.shape[0] == 45
    assert X_test_small.shape[0] == 5
    assert y_train_small.shape[0] == 45
    assert y_test_small.shape[0] == 5


def test_train_model():
    clean_data = get_clean_data()
    model = train_model(clean_data, experiment_name="Test Experiment")

    assert isinstance(model, MultinomialNB)

    # Extract the featuers and targets to valdiate the model
    X, y = get_numpy_X_y(clean_data)
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)
    tfidf = TfidfTransformer(use_idf=True, norm="l2", smooth_idf=True)
    X_tfidf = tfidf.fit_transform(vectorizer.fit_transform(X)).toarray()

    X_train, X_test, y_train, y_test = split_data(X_tfidf, y)
    y_pred = model.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    assert accuracy > 0.7
