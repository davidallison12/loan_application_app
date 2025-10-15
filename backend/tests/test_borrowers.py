import pytest



# ========================================
# Borrowers Specific Unit Test
# ========================================

@pytest.fixture
def mock_borrower_request():
    return {
        "first_name": "John ",
        "last_name": "Doe",
        "address_1": "123 Main St",
        "address_2": "Apt 4B",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "email": "email@email.com",
        "phone": "555-123-4567",
        "ssn": "123-45-6789"
        }


@pytest.fixture
def mock_expected_response():
    return {
        "first_name": "John ",
        "last_name": "Doe",
        "address_1": "123 Main St",
        "address_2": "Apt 4B",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "email": "email@email.com",
        "phone": "555-123-4567"
        }


def test_create_borrower_success_201(client, mock_borrower_request, mock_expected_response):
    """Test creating a borrower successfully returns 201 status code and correct data."""
    
    response = client.post("/api/borrowers", json=mock_borrower_request)   
    json_data = response.get_json()

    assert response.status_code == 201
    # Removing id before comparison
    json_data.pop("borrower_id", None)

    assert json_data == mock_expected_response


def test_create_borrower_duplicate_ssn_409(client, mock_borrower_request):
    """Test creating a borrower with duplicate SSN returns 409 status code."""
    
    # First request should succeed
    response1 = client.post("/api/borrowers", json=mock_borrower_request)
    assert response1.status_code == 201

    # Second request with same SSN should fail
    response2 = client.post("/api/borrowers", json=mock_borrower_request)
    json_data = response2.get_json()

    assert response2.status_code == 409
    assert "error" in json_data
    assert json_data["error"] == "Borrower with this SSN already exists."
