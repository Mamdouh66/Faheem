import pickle
import numpy as np
import polars as pl

from contextlib import asynccontextmanager

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ML_MODELS = dict()


def load_model(
    path_to_model: str,
    path_to_data: pl.DataFrame,
    path_to_vectorizer: str,
    path_to_transformer: str,
):
    with open(path_to_model, "rb") as f:
        model = pickle.load(f)
    with open(path_to_vectorizer, "rb") as f:
        vectorizer = pickle.load(f)
    with open(path_to_transformer, "rb") as f:
        transformer = pickle.load(f)
    ML_MODELS["info"] = pl.read_csv(path_to_data)
    ML_MODELS["vectorizer"] = vectorizer
    ML_MODELS["transformer"] = transformer
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    ML_MODELS["sentiment_analysis_01"] = load_model(
        "notebooks/models/nb_model.pkl",
        "data/out.csv",
        "notebooks/models/vectorizer.pkl",
        "notebooks/models/tfidf_transformer.pkl",
    )
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
