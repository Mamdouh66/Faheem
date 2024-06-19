import pytest
import polars as pl
import pandas as pd
import great_expectations as ge

from faheem.resources.data import get_clean_data


@pytest.fixture(scope="module")
def df():
    clean_data = get_clean_data().to_pandas()
    df = ge.dataset.PandasDataset(clean_data)
    return df
