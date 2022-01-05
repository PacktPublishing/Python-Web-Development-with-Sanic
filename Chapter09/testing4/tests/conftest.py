import pytest
from sanic_testing.reusable import ReusableClient

from ..server import app


@pytest.fixture(scope="session")
def test_client():
    client = ReusableClient(app, host="localhost", port=1234)
    client.run()
    yield client
    client.stop()
