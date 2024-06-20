import pytest

from faheem.config import settings
from faheem.resources.utils import load_model


def get_label(text: str) -> int:
    """Get the label for a given input text."""
    vectorizer, transformer, model = load_model(settings.PATH_TO_MODEL)
    text_vecotrized = vectorizer.transform([text])
    text_transformed = transformer.transform(text_vecotrized)
    predictions_list = model.predict_proba(text_transformed).tolist()[0]
    predicted_label = max(predictions_list)
    label_index = predictions_list.index(predicted_label)
    return label_index


@pytest.mark.parametrize(
    "input_a, input_b, label",
    [
        (
            "ولان بعض الحال يصعب شرحه اثرت صمتا والسكوت مرير",
            "ولان بعض الحال يصعب شرحه اثرت صمتا والصمت متعب",
            0,
        ),
    ],
)
def test_invariance(input_a, input_b, label):
    """INVariance via verb injection (changes should not affect outputs)."""
    label_a = get_label(
        text=input_a,
    )
    label_b = get_label(
        text=input_b,
    )
    assert label_a == label_b == label


@pytest.mark.parametrize(
    "input, label",
    [
        (
            "سعدت بلقياك ياصاحبي",
            1,
        ),
        (
            "حزنت بلقياك ياصاحبي",
            0,
        ),
    ],
)
def test_directional(input, label):
    """DIRectional expectations (changes with known outputs)."""
    prediction = get_label(text=input)
    assert label == prediction


@pytest.mark.parametrize(
    "input, label",
    [
        (
            "ولان بعض الحال يصعب شرحه اثرت صمتا والسكوت مرير",
            0,
        ),
        (
            "ان كان لناس عيد يفرحون به فانت عيدي الذي احيا به فرحا",
            1,
        ),
    ],
)
def test_mft(input, label):
    """Minimum Functionality Tests (simple input/output pairs)."""
    prediction = get_label(text=input)
    assert label == prediction
