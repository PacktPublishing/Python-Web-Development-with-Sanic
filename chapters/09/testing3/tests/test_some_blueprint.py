# test_some_blueprint.py
from unittest.mock import AsyncMock, patch
from aiohttp import request
import pytest
from testing3.path.to.some_blueprint import bp


@pytest.fixture
def app_with_bp(dummy_app):
    dummy_app.blueprint(bp)
    return dummy_app


@pytest.mark.parametrize(
    "input,expected_status",
    (
        (
            {
                "username": "Alice",
                "email": "alice@bob.com",
            },
            201,
        ),
    ),
)
def test_some_blueprint_data_validation(
    app_with_bp,
    mocked_execute,
    input,
    expected_status,
):
    _, response = app_with_bp.test_client.post(
        "/registration",
        json=input,
    )

    assert response.status == expected_status

    if expected_status == 201:
        mocked_execute.assert_awaited_with(
            "INSERT INTO users VALUES ($1, $2);", input["username"], input["email"]
        )
