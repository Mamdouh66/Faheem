import pytest

from faheem.resources.ml.data import preprocess_text


@pytest.mark.parametrize(
    "text, clean_text",
    [
        ("قلتُ لصاحبي، اهلًا بِك", "قلت لصاحبي اهلا بك"),
        ("كثيـــــــــر من الناس", "كثير من الناس"),
        ("إقنع بِمن عندك يقنع بِكَ من عنْدك؛", "اقنع بمن عندك يقنع بك من عندك"),
    ],
)
def test_preprocess_text(text, clean_text):
    assert preprocess_text(text) == clean_text
