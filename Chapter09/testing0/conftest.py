import pytest
from sanic_testing.testing import SanicTestClient

from server import app


@pytest.fixture
def test_client():
    return SanicTestClient(app)
