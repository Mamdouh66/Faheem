import pickle

from contextlib import asynccontextmanager
from typing import Tuple

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ML_MODELS = dict()


def load_model(
    path_to_model: str,
) -> Tuple[CountVectorizer, TfidfTransformer, MultinomialNB]:
    with open(path_to_model, "rb") as f:
        vectorizer, transformer, model = pickle.load(f)
    return vectorizer, transformer, model


@asynccontextmanager
async def lifespan(app: FastAPI):
    vectorizer, transformer, model = load_model("notebooks/models/nb_model.pkl")
    ML_MODELS["vectorizer"] = vectorizer
    ML_MODELS["transformer"] = transformer
    ML_MODELS["sentiment_analysis_01"] = model
    yield
    ML_MODELS.clear()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "I AM ALIVE!!"}


@app.get("/predict")
async def predict(text: str):
    vectorizer = ML_MODELS["vectorizer"]
    transformer = ML_MODELS["transformer"]

    text_vectorized = vectorizer.transform([text])
    text_transformed = transformer.transform(text_vectorized)

    model = ML_MODELS["sentiment_analysis_01"]
    prediction = model.predict(text_transformed)

    return {"prediction": prediction.tolist()[0]}


@app.get("/predict_proba")
async def predict_proba(text: str):
    vectorizer = ML_MODELS["vectorizer"]
    transformer = ML_MODELS["transformer"]

    text_vectorized = vectorizer.transform([text])
    text_transformed = transformer.transform(text_vectorized)

    model = ML_MODELS["sentiment_analysis_01"]
    prediction = model.predict_proba(text_transformed)

    return {"prediction": prediction.tolist()[0]}
