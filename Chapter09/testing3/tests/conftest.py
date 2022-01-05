from importlib import import_module
from unittest.mock import AsyncMock
import pytest
from sanic import Sanic
import testing3.path.to.some_db_connection


@pytest.fixture
def mocked_execute(monkeypatch):
    execute = AsyncMock()
    monkeypatch.setattr(
        testing3.path.to.some_db_connection.FakeDBConnection, "execute", execute
    )
    return execute


@pytest.fixture
def dummy_app():
    app = Sanic("DummyApp")

    import_module("testing3.path.to.some_startup")
    return app
