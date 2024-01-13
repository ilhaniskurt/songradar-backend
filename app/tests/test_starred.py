from pytest import fixture

from .test_client import auth_headers, client

valid = [
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 2021,
        "month": 6,
        "day": 25,
    },
    {
        "name": "Naked",
        "artists": "Doja Cat",
        "year": 2021,
        "month": 6,
        "day": 25,
    },
]


@fixture(scope="module")
def ids(auth_headers: auth_headers):
    response = client.post(
        "/albums",
        headers=auth_headers[0],
        json={
            "name": "Planet Her",
            "artists": "Doja Cat",
            "year": 2021,
            "month": 6,
            "day": 25,
        },
    )

    assert response.status_code == 200
    album_id = response.json()["id"]

    ids = []
    for album in valid:
        album.update({"album_id": album_id})
        response = client.post(
            "/songs",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 200
        data = response.json()
        ids.append(data["id"])

    yield ids

    client.delete("/albums/" + album_id, headers=auth_headers[0])


def test_read_empty(auth_headers: auth_headers):
    response = client.get("/starred", headers=auth_headers[0])

    assert response.status_code == 200
    assert response.json() == []


def test_add_without_auth():
    response = client.put("/starred/NULL")

    assert response.status_code == 401


def test_add_invalid(auth_headers: auth_headers):
    response = client.put("/starred/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_add(auth_headers: auth_headers, ids: ids):
    response = client.put("/starred/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()[0]

    assert data["name"] == "Need to Know"
    assert data["artists"] == "Doja Cat"
    assert data["year"] == 2021
    assert data["month"] == 6
    assert data["day"] == 25


def test_add_duplicate(auth_headers: auth_headers, ids: ids):
    response = client.put("/starred/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 400


def test_read(auth_headers: auth_headers):
    response = client.get("/starred", headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()[0]

    assert data["name"] == "Need to Know"
    assert data["artists"] == "Doja Cat"
    assert data["year"] == 2021
    assert data["month"] == 6
    assert data["day"] == 25


def test_delete_song_without_auth():
    response = client.delete("/starred/NULL")

    assert response.status_code == 401


def test_delete_song_invalid(auth_headers: auth_headers):
    response = client.delete("/starred/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_delete_song(auth_headers: auth_headers, ids: ids):
    response = client.delete("/starred/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 200
    assert response.json() == []


def test_delete_song_nonexist(auth_headers: auth_headers, ids: ids):
    response = client.delete("/starred/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 400
