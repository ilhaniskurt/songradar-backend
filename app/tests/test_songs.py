from pytest import fixture

from .test_client import auth_headers, client


@fixture(scope="module")
def album_id(auth_headers: auth_headers):
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
    id = response.json()["id"]

    yield id

    client.delete("/albums/" + id, headers=auth_headers[0])


invalid_day = [
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 2016,
        "month": 12,
        "day": 32,
    },
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 2016,
        "month": 12,
        "day": 0,
    },
]

invalid_month = [
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 2016,
        "month": 13,
        "day": 1,
    },
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 2016,
        "month": 0,
        "day": 1,
    },
]

invalid_year = [
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 4444,
        "month": 12,
        "day": 1,
    },
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 0,
        "month": 12,
        "day": 1,
    },
    {
        "name": "Need to Know",
        "artists": "Doja Cat",
        "year": 1899,
        "month": 12,
        "day": 1,
    },
]

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


def test_create_without_auth():
    response = client.post(
        "/songs",
    )
    assert response.status_code == 401


def test_create_with_invalid_day(auth_headers: auth_headers):
    for album in invalid_day:
        response = client.post(
            "/songs",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_create_with_invalid_month(auth_headers: auth_headers):
    for album in invalid_month:
        response = client.post(
            "/songs",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_create_with_invalid_year(auth_headers: auth_headers):
    for album in invalid_year:
        response = client.post(
            "/songs",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_create_with_invalid_id(auth_headers: auth_headers):
    album = valid[0]
    album.update({"album_id": "NULL"})
    response = client.post(
        "/songs",
        headers=auth_headers[0],
        json=album,
    )
    assert response.status_code == 404


def test_create_with_wrong_auth(auth_headers: auth_headers, album_id: album_id):
    album = valid[0]
    album.update({"album_id": album_id})
    response = client.post(
        "/songs",
        headers=auth_headers[1],
        json=album,
    )
    assert response.status_code == 400


def test_read_empty():
    response = client.get("/songs")

    assert response.status_code == 200
    assert response.json() == []


id = ""


def test_create(auth_headers: auth_headers, album_id: album_id):
    global id
    for album in valid:
        album.update({"album_id": album_id})
        response = client.post(
            "/songs",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 200
        data = response.json()
        id = data["id"]
        assert data["name"] == album["name"]
        assert data["artists"] == album["artists"]
        assert data["year"] == album["year"]
        assert data["month"] == album["month"]
        assert data["day"] == album["day"]
        assert data["album"] == "Planet Her"


def test_read():
    response = client.get("/songs")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for i, album in enumerate(data):
        assert album["name"] == valid[i]["name"]
        assert album["artists"] == valid[i]["artists"]
        assert album["year"] == valid[i]["year"]
        assert album["month"] == valid[i]["month"]
        assert album["day"] == valid[i]["day"]
        assert album["album"] == "Planet Her"


def test_read_recent():
    response = client.get("/songs/recent")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for i, album in enumerate(data):
        assert album["name"] == valid[1 - i]["name"]
        assert album["artists"] == valid[1 - i]["artists"]
        assert album["year"] == valid[1 - i]["year"]
        assert album["month"] == valid[1 - i]["month"]
        assert album["day"] == valid[1 - i]["day"]
        assert album["album"] == "Planet Her"


def test_user_without_auth():
    response = client.get("/songs/user")

    assert response.status_code == 401


def test_user_empty(auth_headers: auth_headers):
    response = client.get("/songs/user", headers=auth_headers[1])

    assert response.status_code == 200
    assert response.json() == []


def test_count():
    response = client.get("/songs/count")

    assert response.status_code == 200
    assert response.json() == 2


def test_find_error():
    response = client.get("/songs/find/NULL")
    assert response.status_code == 404


def test_find():
    response = client.get("/songs/find/" + id)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == valid[1]["name"]
    assert data["artists"] == valid[1]["artists"]
    assert data["year"] == valid[1]["year"]
    assert data["month"] == valid[1]["month"]
    assert data["day"] == valid[1]["day"]
    assert data["album"] == "Planet Her"


def test_search_name():
    response = client.get("/songs/search_name?name=naked")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == valid[1]["name"]
    assert data["artists"] == valid[1]["artists"]
    assert data["year"] == valid[1]["year"]
    assert data["month"] == valid[1]["month"]
    assert data["day"] == valid[1]["day"]
    assert data["album"] == "Planet Her"


def test_search_name_empty():
    response = client.get("/songs/search_name?name=NULL")

    assert response.status_code == 200
    assert response.json() == []


def test_search_artist():
    response = client.get("/songs/search_artist?artist=doja")

    assert response.status_code == 200
    data = response.json()[1]
    assert data["name"] == valid[1]["name"]
    assert data["artists"] == valid[1]["artists"]
    assert data["year"] == valid[1]["year"]
    assert data["month"] == valid[1]["month"]
    assert data["day"] == valid[1]["day"]
    assert data["album"] == "Planet Her"


def test_search_artist_empty():
    response = client.get("/songs/search_artist?artist=NULL")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_without_auth():
    response = client.delete("/songs/" + id)

    assert response.status_code == 401


def test_delete_wrong_auth(auth_headers: auth_headers):
    response = client.delete("/songs/" + id, headers=auth_headers[1])

    assert response.status_code == 400


def test_delete_invalid(auth_headers: auth_headers):
    response = client.delete("/songs/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_delete(auth_headers: auth_headers):
    response = client.delete("/songs/" + id, headers=auth_headers[0])

    assert response.status_code == 200


def test_find_deleted():
    response = client.get("/songs/find/" + id)

    assert response.status_code == 404


def test_cascade(auth_headers: auth_headers, album_id: album_id):
    response = client.delete("/albums/" + album_id, headers=auth_headers[0])

    assert response.status_code == 200

    response = client.get("/songs/count")

    assert response.status_code == 200
    assert response.json() == 0
