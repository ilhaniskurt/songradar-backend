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


def test_user_empty(auth_headers: auth_headers):
    response = client.get("/playlists/user", headers=auth_headers[0])

    assert response.status_code == 200
    assert response.json() == []


def test_create_without_auth():
    response = client.post("/playlists", json={"name": "test"})

    assert response.status_code == 401


def test_create(auth_headers: auth_headers):
    response = client.post("/playlists", headers=auth_headers[0], json={"name": "test"})

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "test"
    assert data["id"] == 1
    assert data["songs"] == []


def test_user(auth_headers: auth_headers):
    response = client.get("/playlists/user", headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()[0]

    assert data["name"] == "test"
    assert data["id"] == 1
    assert data["songs"] == []


def test_rename_without_auth():
    response = client.put("/playlists/NULL?new_name=rock")

    assert response.status_code == 401


def test_rename_wrong_auth(auth_headers: auth_headers):
    response = client.put("/playlists/1?new_name=rock", headers=auth_headers[1])

    assert response.status_code == 400


def test_rename(auth_headers: auth_headers):
    response = client.put("/playlists/1?new_name=rock", headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "rock"
    assert data["songs"] == []


def test_find_error():
    response = client.get("/playlists/NULL")

    assert response.status_code == 404


def test_find():
    response = client.get("/playlists/" + str(1))

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "rock"
    assert data["songs"] == []


def test_add_without_auth():
    response = client.put("/playlists/1/NULL")

    assert response.status_code == 401


def test_add_wrong_auth(auth_headers: auth_headers):
    response = client.put("/playlists/1/NULL", headers=auth_headers[1])

    assert response.status_code == 400


def test_add_invalid(auth_headers: auth_headers):
    response = client.put("/playlists/1/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_add(auth_headers: auth_headers, ids: ids):
    response = client.put("/playlists/1/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "rock"
    assert data["songs"][0]["name"] == "Need to Know"
    assert data["songs"][0]["artists"] == "Doja Cat"
    assert data["songs"][0]["year"] == 2021
    assert data["songs"][0]["month"] == 6
    assert data["songs"][0]["day"] == 25


def test_add_duplicate(auth_headers: auth_headers, ids: ids):
    response = client.put("/playlists/1/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 400


def test_delete_song_without_auth():
    response = client.delete("/playlists/1/NULL")

    assert response.status_code == 401


def test_delete_song_wrong_auth(auth_headers: auth_headers):
    response = client.delete("/playlists/1/NULL", headers=auth_headers[1])

    assert response.status_code == 400


def test_delete_song_invalid(auth_headers: auth_headers):
    response = client.delete("/playlists/1/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_delete_song(auth_headers: auth_headers, ids: ids):
    response = client.delete("/playlists/1/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "rock"
    assert data["songs"] == []


def test_delete_song_nonexist(auth_headers: auth_headers, ids: ids):
    response = client.delete("/playlists/1/" + ids[0], headers=auth_headers[0])

    assert response.status_code == 400


def test_delete_without_auth():
    response = client.delete("/playlists/1")

    assert response.status_code == 401


def test_delete_wrong_auth(auth_headers: auth_headers):
    response = client.delete("/playlists/1", headers=auth_headers[1])

    assert response.status_code == 400


def test_delete_invalid(auth_headers: auth_headers):
    response = client.delete("/playlists/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_delete(auth_headers: auth_headers):
    response = client.delete("/playlists/1", headers=auth_headers[0])

    assert response.status_code == 200
