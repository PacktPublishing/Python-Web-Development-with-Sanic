from sanic import Sanic


def test_sample(app: Sanic):
    request, response = app.test_client.get("/")

    assert response.status == 200
