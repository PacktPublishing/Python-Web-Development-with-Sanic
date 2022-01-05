import pytest
from sanic import Sanic


@pytest.fixture
def dummy_app():
    return Sanic("DummyApp")
