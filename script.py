import ast
from collections import OrderedDict

import pandas as pd
import requests

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


def get_songs(filenames: list) -> pd.DataFrame:
    print("Reading csvs..")
    na = ["", "NaN"]
    df = pd.concat(
        (pd.read_csv(file, na_values=na, keep_default_na=False) for file in filenames),
        ignore_index=True,
    )
    print("Reading csv finished!")
    return df


def create_songs(df: pd.DataFrame, start: int = 0) -> None:
    print("Sending requests to api to create songs..")
    counter = start
    for row in df[start:].itertuples():
        date = str(row.release_date).split("-")
        json_data = {
            "id": row.id,
            "name": row.name,
            "album": row.album,
            "album_id": row.album_id,
            "artists": row.artists,
            "artist_ids": row.artist_ids,
            "track_number": row.track_number,
            "disc_number": row.disc_number,
            "explicit": row.explicit,
            "danceability": row.danceability,
            "energy": row.energy,
            "key": row.key,
            "loudness": row.loudness,
            "mode": row.mode,
            "speechiness": row.speechiness,
            "acousticness": row.acousticness,
            "instrumentalness": row.instrumentalness,
            "liveness": row.liveness,
            "valence": row.valence,
            "tempo": row.tempo,
            "duration_ms": row.duration_ms,
            "time_signature": row.time_signature,
            "year": date[0],
            "month": 1 if len(date) < 2 else date[1],
            "day": 1 if len(date) < 3 else date[2],
        }
        requests.post(
            "http://localhost:8000/debug/songs", headers=headers, json=json_data
        )
        counter
    print("Done!")


def create_albums(df: pd.DataFrame, start: int = 0):
    print("Sending requests to api to create songs..")
    unique_album_ids = df["album_id"].unique().tolist()

    for album_id in unique_album_ids[start:]:
        album_df = df[df["album_id"] == album_id]
        name = album_df["album"].iloc[0]

        artists = list(
            OrderedDict.fromkeys(
                artist
                for sublist in album_df["artists"].apply(ast.literal_eval)
                for artist in sublist
            )
        )
        artist_ids = list(
            OrderedDict.fromkeys(
                artist
                for sublist in album_df["artist_ids"].apply(ast.literal_eval)
                for artist in sublist
            )
        )

        date = pd.to_datetime(album_df["release_date"]).max()

        json_data = {
            "id": album_id,
            "name": name,
            "artists": str(artists),
            "artist_ids": str(artist_ids),
            "number_of_tracks": len(album_df),
            "explicit": bool(album_df["explicit"].any()),
            "danceability": album_df["danceability"].mean(),
            "energy": album_df["energy"].mean(),
            "key": int(album_df["key"].mode().iloc[0]),
            "loudness": album_df["loudness"].mean(),
            "mode": int(album_df["mode"].mode().iloc[0]),
            "speechiness": album_df["speechiness"].mean(),
            "acousticness": album_df["acousticness"].mean(),
            "instrumentalness": album_df["instrumentalness"].mean(),
            "liveness": album_df["liveness"].mean(),
            "valence": album_df["valence"].mean(),
            "tempo": album_df["tempo"].mean(),
            "duration_ms": int(album_df["duration_ms"].sum()),
            "time_signature": int(album_df["time_signature"].mode().iloc[0]),
            "year": date.year,
            "month": date.month,
            "day": date.day,
        }
        requests.post(
            "http://localhost:8000/debug/albums", headers=headers, json=json_data
        )
    print("Done!")


if __name__ == "__main__":
    csv_files = ["songs_0.csv", "songs_1.csv", "songs_2.csv", "songs_3.csv"]
    # pd.set_option("display.max_columns", None)
    df = get_songs(csv_files)
    create_songs(df)
    create_albums(df)
