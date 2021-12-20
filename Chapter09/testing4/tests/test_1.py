from sanic_testing.reusable import ReusableClient

from ..server import app


def test_reusable_context():
    client = ReusableClient(app, host="localhost", port=4567)

    with client:
        _, response = client.get("/")
        assert response.json == 0

        _, response = client.get("/")
        assert response.json == 1

        _, response = client.get("/")
        assert response.json == 2


def test_reusable_fixture(test_client):
    _, response = test_client.get("/")
    assert response.json == 0

    _, response = test_client.get("/")
    assert response.json == 1

    _, response = test_client.get("/")
    assert response.json == 2
