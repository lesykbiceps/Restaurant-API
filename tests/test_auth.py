def test_register(client, app):
    assert client.post(
        '/auth/registration',
        json={
            "name": "Test",
            "username": " test",
            "password": "test123pass",
            "email": "test1email",
            "is_admin": True,
        }
    ).json["message"] == 'User  test was created'


def test_user_already_exists(client, app):
    assert client.post(
        '/auth/registration',
        json={
            "name": "Test",
            "username": " test",
            "password": "test123pass",
            "email": "test1email",
            "is_admin": True
        }
    ).json["message"] == "User  test already exists"


def test_login_fail(client, app):
    assert client.post(
        '/auth/login',
        json={
            "password": 23,
        }
    ).json["message"] == 'Please, provide "username" and "password" in body.'
