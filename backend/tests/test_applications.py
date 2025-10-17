from datetime import datetime
from unittest.mock import patch

import pytest

# Fixtures for application tests


@pytest.fixture
def mock_application_request():
    return {
        "borrower": {
            "first_name": "John ",
            "last_name": "Doe",
            "address_1": "123 Main St",
            "address_2": "Apt 4B",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345",
            "email": "email@email.com",
            "phone": "555-123-4567",
            "ssn": "123-45-6789",
        },
        "requested_amount": 15000.00,
    }


@pytest.fixture
def mock_expected_response():
    return {
        "application_id": 1,
        "borrower_id": 1,
        "requested_amount": 15000.00,
        "open_credit_lines": None,  # This will be dynamic
        "approved_amount": 15000.00,
        "interest_rate": None,
        "term_months": None,
        "monthly_payment": None,
        "status": "Approved",
        "reason": None,
        "borrower": {
            "borrower_id": 1,
            "first_name": "John ",
            "last_name": "Doe",
            "address_1": "123 Main St",
            "address_2": "Apt 4B",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345",
            "email": "email@email.com",
            "phone": "555-123-4567",
            "created_at": "2025-10-16T12:00:00",
            "updated_at": "2025-10-16T12:00:00",
        },
        "created_at": "2025-10-16T12:00:00",
        "updated_at": "2025-10-16T12:00:00",
    }


@pytest.fixture
def mock_expected_denied_response():
    return {
        "application_id": 1,
        "borrower_id": 1,
        "requested_amount": 15000.00,
        "open_credit_lines": 51,
        "approved_amount": None,
        "interest_rate": None,
        "term_months": None,
        "monthly_payment": None,
        "status": "Denied",
        "reason": None,
        "borrower": {
            "borrower_id": 1,
            "first_name": "John ",
            "last_name": "Doe",
            "address_1": "123 Main St",
            "address_2": "Apt 4B",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345",
            "email": "email@email.com",
            "phone": "555-123-4567",
            "created_at": "2025-10-16T12:00:00",
            "updated_at": "2025-10-16T12:00:00",
        },
        "created_at": "2025-10-16T12:00:00",
        "updated_at": "2025-10-16T12:00:00",
    }


# ========================================
# Application Specific Unit Test
# ========================================


@patch("models.datetime")
@patch("routes.random.randint", return_value=25)  # Force open_credit_lines = 25
def test_create_application_success_24_month_201(
    mock_randint,
    mock_datetime,
    client,
    mock_application_request,
    mock_expected_response,
):
    """
    Test creating a loan application successfully returns 201 status code and correct data.
    Scenario: Credit lines <=50 and >=10 = a 24-month term and 20% interest applies
    """

    # Set fixed datetime for consistency in tests
    fixed_time = datetime(2025, 10, 16, 12, 0, 0)
    mock_datetime.now.return_value = fixed_time
    mock_datetime.now.return_value = fixed_time
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Make the API call
    response = client.post("/api/applications", json=mock_application_request)
    json_data = response.get_json()

    # Validate response
    assert response.status_code == 201

    expected_response = mock_expected_response
    expected_response["open_credit_lines"] = 25
    expected_response["term_months"] = 24
    expected_response["interest_rate"] = 0.20
    expected_response["monthly_payment"] = 763.44

    assert json_data == expected_response


@patch("models.datetime")
@patch("routes.random.randint", return_value=9)  # Force open_credit_lines = 25
def test_create_application_success_36_month_201(
    mock_randint,
    mock_datetime,
    client,
    mock_application_request,
    mock_expected_response,
):
    """
    Test creating a loan application successfully returns 201 status code and correct data.
    Scenario: Credit lines <10 = a 36-month term and 10% interest applies
    """

    # Set fixed datetime for consistency in tests
    fixed_time = datetime(2025, 10, 16, 12, 0, 0)
    mock_datetime.now.return_value = fixed_time
    mock_datetime.now.return_value = fixed_time
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Make the API call
    response = client.post("/api/applications", json=mock_application_request)
    json_data = response.get_json()

    # Validate response
    assert response.status_code == 201

    expected_response = mock_expected_response
    expected_response["open_credit_lines"] = 9
    expected_response["term_months"] = 36
    expected_response["interest_rate"] = 0.10
    expected_response["monthly_payment"] = 484.01

    assert json_data == expected_response


@patch("models.datetime")
@patch("routes.random.randint", return_value=51)  # Force open_credit_lines = 50
def test_create_application_denied_too_many_credit_lines_201(
    mock_randint,
    mock_datetime,
    client,
    mock_application_request,
    mock_expected_denied_response,
):
    """
    Test creating a loan application that gets denied due to too many open credit lines.
    Scenario: Credit lines >50 = Denied
    """

    # Set fixed datetime for consistency in tests
    fixed_time = datetime(2025, 10, 16, 12, 0, 0)
    mock_datetime.now.return_value = fixed_time
    mock_datetime.now.return_value = fixed_time
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Make the API call
    response = client.post("/api/applications", json=mock_application_request)
    json_data = response.get_json()

    # Validate response
    assert response.status_code == 201

    expected_response = mock_expected_denied_response
    expected_response["open_credit_lines"] = 51
    expected_response["reason"] = "Too many open credit lines."

    assert json_data == expected_response
