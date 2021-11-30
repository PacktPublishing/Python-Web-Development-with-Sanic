def test_sample(test_client):
    request, response = test_client.get("/")

    assert response.status == 200
