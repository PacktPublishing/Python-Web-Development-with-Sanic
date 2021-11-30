import pytest

from server import app as application_instance


@pytest.fixture
def app():
    return application_instance
