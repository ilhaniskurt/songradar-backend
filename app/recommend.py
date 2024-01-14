from contextlib import asynccontextmanager
from functools import lru_cache

import pandas as pd
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.sql import crud, models, schemas
from app.utils import dependencies
from app.utils.config import settings

router = APIRouter(prefix="/recommend", tags=["recommend"])
default_songs = []


@asynccontextmanager
async def recommend_lifespan(app: FastAPI):
    global default_songs
    print("INFO:     Loading songs from csv.. Might take a second.")
    na = ["", "NaN"]
    default_songs = pd.concat(
        (
            pd.read_csv(file, na_values=na, keep_default_na=False)
            for file in settings.songfiles
        ),
        ignore_index=True,
    )
    print("INFO:     Done!")
    yield


# This takes longer
@asynccontextmanager
async def recommend_lifespan_with_query(app: FastAPI):
    global default_songs
    print("INFO:     Loading songs from csv.. Might take a while.")
    with dependencies.get_db() as db:
        default_songs = crud.get_all_defualt_songs(db)
        print("INFO:     Done!")
        yield


def get_features_from_model(model: models.Song | models.Album):
    features = [
        [
            model.danceability,
            model.speechiness,
            model.acousticness,
            model.instrumentalness,
            model.liveness,
            model.valence,
            model.tempo,
            model.loudness,
            model.mode,
            model.key,
        ]
    ]
    return features


@lru_cache
def get_features_from_df():
    features = default_songs[
        [
            "danceability",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "loudness",
            "mode",
            "key",
        ]
    ]
    return features


@router.get("/song/{id}", response_model=list[schemas.Song])
def recommend_song_from_song(
    id: str,
    recommend: int = 10,
    db: Session = Depends(dependencies.get_db),
):
    song = crud.get_song_by_id(db, id)
    if not song:
        raise HTTPException(status_code=404, detail="Invalid song id: " + id)

    if song.owner_id != 0:
        raise HTTPException(
            status_code=400,
            detail="User registered songs are incompatible for recommendation",
        )

    target_song_features = get_features_from_model(song)
    all_song_features = get_features_from_df()

    similarities = cosine_similarity(target_song_features, all_song_features)[0]

    recommendations = []

    if len(similarities) < 1 + recommend:
        raise HTTPException(
            status_code=404,
            detail="Could not find the required amount of recommendation(s)",
        )

    for i in range(recommend):
        similarities[similarities.argmax()] = -1
        # max_similarity = similarities.max()
        recommended_song_id = default_songs.loc[similarities.argmax(), "id"]

        recommendations.append(crud.get_song_by_id(db, recommended_song_id))

    return recommendations
