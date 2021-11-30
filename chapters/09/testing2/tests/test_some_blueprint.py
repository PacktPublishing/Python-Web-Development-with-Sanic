# test_some_blueprint.py
import pytest
from testing2.path.to.some_blueprint import bp


@pytest.fixture
def app_with_bp(dummy_app):
    dummy_app.blueprint(bp)
    return dummy_app


def test_some_blueprint_make_square(app_with_bp):
    _, response = app_with_bp.test_client.post(
        "/some/validation",
        json={
            "a_string": "hello",
            "an_int": "999",
        },
    )

    assert not any(value == "MISSING" for value in response.json.values())
    assert len(response.json) == 2


def test_some_blueprint_correct_data(app_with_bp):
    _, response = app_with_bp.test_client.post(
        "/some/validation",
        json={
            "a_string": "hello",
            "an_int": 999,
        },
    )

    assert response.status == 200


def test_some_blueprint_bad_data(app_with_bp):
    _, response = app_with_bp.test_client.post(
        "/some/validation",
        json={
            "a_string": "hello",
            "an_int": 999,
            "a_bool": True,
        },
    )

    assert response.status == 400


@pytest.mark.parametrize(
    "input,has_missing,expected_status",
    (
        (
            {
                "a_string": "hello",
            },
            True,
            400,
        ),
        (
            {
                "a_string": "hello",
                "an_int": "999",
            },
            False,
            400,
        ),
        (
            {
                "a_string": "hello",
                "an_int": 999,
            },
            False,
            200,
        ),
        (
            {
                "a_string": "hello",
                "an_int": 999,
                "a_bool": True,
            },
            False,
            400,
        ),
    ),
)
def test_some_blueprint_data_validation(
    app_with_bp,
    input,
    has_missing,
    expected_status,
):
    _, response = app_with_bp.test_client.post(
        "/some/validation",
        json=input,
    )

    assert (
        any(value == "MISSING" for value in response.json.values())
        is has_missing
    )
    assert response.status == expected_status
