from .test_client import auth_headers, client

invalid_day = [
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 2016,
        "month": 12,
        "day": 32,
    },
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 2016,
        "month": 12,
        "day": 0,
    },
]

invalid_month = [
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 2016,
        "month": 13,
        "day": 1,
    },
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 2016,
        "month": 0,
        "day": 1,
    },
]

invalid_year = [
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 4444,
        "month": 12,
        "day": 1,
    },
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 0,
        "month": 12,
        "day": 1,
    },
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 1899,
        "month": 12,
        "day": 1,
    },
]

valid = [
    {
        "name": "Positions",
        "artists": "Ariana Grande",
        "year": 2020,
        "month": 10,
        "day": 30,
    },
    {
        "name": "Planet Her",
        "artists": "Doja Cat",
        "year": 2021,
        "month": 6,
        "day": 25,
    },
]


def test_create_without_auth():
    response = client.post(
        "/albums",
    )
    assert response.status_code == 401


def test_create_with_invalid_day(auth_headers: auth_headers):
    for album in invalid_day:
        response = client.post(
            "/albums",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_create_with_invalid_month(auth_headers: auth_headers):
    for album in invalid_month:
        response = client.post(
            "/albums",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_create_with_invalid_year(auth_headers: auth_headers):
    for album in invalid_year:
        response = client.post(
            "/albums",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 400


def test_read_empty():
    response = client.get("/albums")

    assert response.status_code == 200
    assert response.json() == []


def test_create(auth_headers: auth_headers):
    for album in valid:
        response = client.post(
            "/albums",
            headers=auth_headers[0],
            json=album,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == album["name"]
        assert data["artists"] == album["artists"]
        assert data["year"] == album["year"]
        assert data["month"] == album["month"]
        assert data["day"] == album["day"]


def test_read():
    response = client.get("/albums")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for i, album in enumerate(data):
        assert album["name"] == valid[i]["name"]
        assert album["artists"] == valid[i]["artists"]
        assert album["year"] == valid[i]["year"]
        assert album["month"] == valid[i]["month"]
        assert album["day"] == valid[i]["day"]


def test_user_without_auth():
    response = client.get("/albums/user")

    assert response.status_code == 401


def test_user_empty(auth_headers: auth_headers):
    response = client.get("/albums/user", headers=auth_headers[1])

    assert response.status_code == 200
    assert response.json() == []


def test_user(auth_headers: auth_headers):
    response = client.get("/albums/user", headers=auth_headers[0])

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for i, album in enumerate(data):
        assert album["name"] == valid[i]["name"]
        assert album["artists"] == valid[i]["artists"]
        assert album["year"] == valid[i]["year"]
        assert album["month"] == valid[i]["month"]
        assert album["day"] == valid[i]["day"]


def test_recent():
    response = client.get("/albums/recent")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    for i, album in enumerate(data):
        assert album["name"] == valid[1 - i]["name"]
        assert album["artists"] == valid[1 - i]["artists"]
        assert album["year"] == valid[1 - i]["year"]
        assert album["month"] == valid[1 - i]["month"]
        assert album["day"] == valid[1 - i]["day"]


id = ""


def test_search_name():
    response = client.get("/albums/search_name?name=positions")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == valid[0]["name"]
    assert data["artists"] == valid[0]["artists"]
    assert data["year"] == valid[0]["year"]
    assert data["month"] == valid[0]["month"]
    assert data["day"] == valid[0]["day"]
    global id
    id = data["id"]


def test_search_name_empty():
    response = client.get("/albums/search_name?name=NULL")

    assert response.status_code == 200
    assert response.json() == []


def test_search_artist():
    response = client.get("/albums/search_artist?artist=doja")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == valid[1]["name"]
    assert data["artists"] == valid[1]["artists"]
    assert data["year"] == valid[1]["year"]
    assert data["month"] == valid[1]["month"]
    assert data["day"] == valid[1]["day"]


def test_search_artist_empty():
    response = client.get("/albums/search_artist?artist=NULL")

    assert response.status_code == 200
    assert response.json() == []


def test_count():
    response = client.get("/albums/count")

    assert response.status_code == 200
    assert response.json() == 2


def test_find_error():
    response = client.get("/albums/find/NULL")
    assert response.status_code == 404


def test_find():
    response = client.get("/albums/find/" + id)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == valid[0]["name"]
    assert data["artists"] == valid[0]["artists"]
    assert data["year"] == valid[0]["year"]
    assert data["month"] == valid[0]["month"]
    assert data["day"] == valid[0]["day"]


def test_delete_without_auth():
    response = client.delete("/albums/" + id)

    assert response.status_code == 401


def test_delete_wrong_auth(auth_headers: auth_headers):
    response = client.delete("/albums/" + id, headers=auth_headers[1])

    assert response.status_code == 400


def test_delete_invalid(auth_headers: auth_headers):
    response = client.delete("/albums/NULL", headers=auth_headers[0])

    assert response.status_code == 404


def test_delete(auth_headers: auth_headers):
    response = client.delete("/albums/" + id, headers=auth_headers[0])

    assert response.status_code == 200


def test_find_deleted():
    response = client.get("/albums/find/" + id)

    assert response.status_code == 404
