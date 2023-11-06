from .test_client import client

valid_sign_ups = [
    {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "Test.1234",
    },
    {
        "username": "metekerem",
        "email": "kerem@gmail.com",
        "password": "Kerem@123",
    },
]

invalid_sign_ups = [
    {
        "username": "",
        "email": "",
        "password": "",
    },
    {
        "username": "testuser1",
        "email": "",
        "password": "",
    },
    {
        "username": "",
        "email": "test@hotmail.com",
        "password": "",
    },
    {
        "username": "",
        "email": "",
        "password": "Kerem@123",
    },
    {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "Test.1234",
    },
    {
        "username": "1testsa",
        "email": "test@outlook.com",
        "password": "Test.1234",
    },
    {
        "username": "testuser3",
        "email": "test@example.com",
        "password": "Test.1234",
    },
    {
        "username": "testuser4",
        "email": "_test1@e!xample.com.",
        "password": "Test.1234",
    },
]


def test_sign_up():
    for i, value in enumerate(valid_sign_ups):
        response = client.post(
            "/auth/sign_up",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json=value,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == value["username"]
        assert data["email"] == value["email"]
        assert data["id"] == i + 1


def test_sign_up_error():
    for value in invalid_sign_ups:
        response = client.post(
            "/auth/sign_up",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json=value,
        )
        assert response.status_code == 400


def test_sign_in():
    for value in valid_sign_ups:
        response = client.post(
            "/auth/sign_in",
            headers={"accept": "application/json"},
            data={"username": value["username"], "password": value["password"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"
        value["access_token"] = data["access_token"]


def test_me():
    for i, value in enumerate(valid_sign_ups):
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer " + value["access_token"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == value["username"]
        assert data["email"] == value["email"]
        assert data["id"] == i + 1
