import pytest
import polars as pl

from faheem.config import settings
from faheem.resources.ml.data import load_data


@pytest.fixture
def get_dataset():
    paths = settings.PATH_TO_DATA
    keys = list(paths.keys())

    train_neg = load_data(paths[keys[0]], 0)
    train_pos = load_data(paths[keys[1]], 1)
    test_neg = load_data(paths[keys[2]], 0)
    test_pos = load_data(paths[keys[3]], 1)
    train_df = pl.concat([train_neg, train_pos])
    test_df = pl.concat([test_neg, test_pos])

    dataframe = pl.concat([train_df, test_df])
    return dataframe
