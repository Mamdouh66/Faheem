import csv
import re
import string

import polars as pl

from faheem.config import settings


def load_data(file_path: str, label: int) -> pl.DataFrame:
    """
    Load data from a TSV file and changing it to a CSV file to easily read from.

    Args:
        file_path (str): The path to the TSV file.
        label (int): The label to assign to each tweet (0 for negative, 1 for positive).

    Returns:
        pl.DataFrame: A Polars DataFrame containing tweets and their labels.
    """
    rows = []
    with open(file_path, newline="", encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        for row in reader:
            rows.append([row[1], label])
    return pl.DataFrame(rows, schema=["tweet", "label"])


def preprocess_text(text: str) -> str:
    """
    Preprocess a tweet by removing mentions, URLs, punctuation, emojis, diacritics,
    and extra spaces, normalizing Arabic text, and removing repeated characters.

    Args:
        text (str): The tweet text to preprocess.

    Returns:
        str: The cleaned and normalized tweet text.
    """
    arabic_diacritics = re.compile(
        """
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida

                         """,
        re.VERBOSE,
    )

    arabic_punctuations = """`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ"""
    english_punctuations = string.punctuation
    punctuations_list = arabic_punctuations + english_punctuations

    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)

    text = re.sub(arabic_diacritics, "", text)

    translator = str.maketrans("", "", punctuations_list)
    text = text.translate(translator)

    text = re.sub(r"(.)\1+", r"\1", text)

    return text


def get_clean_data(
    file_paths: dict | None = None, default: bool = True
) -> pl.DataFrame:
    """
    Load, process Arabic tweet datasets into a single cleaned DataFrame.

    Args:
        `file_paths` (dict): A dictionary containing file paths to the datasets.
            The expected keys are:\n
                - "train_arabic_negative_tweets" (str): Path to the training dataset with negative tweets.
                - "train_arabic_positive_tweets" (str): Path to the training dataset with positive tweets.
                - "test_arabic_negative_tweets" (str): Path to the testing dataset with negative tweets.
                - "test_arabic_positive_tweets" (str): Path to the testing dataset with positive tweets.
        `default` (bool): If True, use default file paths from settings.PATH_TO_DATA. If False, use provided file paths.

    Returns:
        `pl.DataFrame`: A Polars DataFrame containing the concatenated and cleaned tweet datasets. The DataFrame
        includes an additional column 'cleaned_tweet' which contains the preprocessed text of the tweets.
    """
    if default and not file_paths:
        file_paths = settings.PATH_TO_DATA
        train_neg = load_data(file_paths["train_arabic_negative_tweets"], 0)
        train_pos = load_data(file_paths["train_arabic_positive_tweets"], 1)
        test_neg = load_data(file_paths["test_arabic_negative_tweets"], 0)
        test_pos = load_data(file_paths["test_arabic_positive_tweets"], 1)
    else:
        keys = list(file_paths.keys())
        train_neg = load_data(file_paths[keys[0]], 0)
        train_pos = load_data(file_paths[keys[1]], 1)
        test_neg = load_data(file_paths[keys[2]], 0)
        test_pos = load_data(file_paths[keys[3]], 1)

    train_df = pl.concat([train_neg, train_pos])
    test_df = pl.concat([test_neg, test_pos])

    dataframe = pl.concat([train_df, test_df])

    df = dataframe.with_columns(
        [
            pl.col("tweet")
            .map_elements(preprocess_text, return_dtype=str)
            .alias("cleaned_tweet")
        ],
    )

    return df
