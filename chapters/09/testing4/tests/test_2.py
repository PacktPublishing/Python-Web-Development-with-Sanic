def test_reusable_fixture(test_client):
    _, response = test_client.get("/")
    assert response.json == 3

    _, response = test_client.get("/")
    assert response.json == 4

    _, response = test_client.get("/")
    assert response.json == 5
