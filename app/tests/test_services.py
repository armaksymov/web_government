import pytest
from app.services.auth_service import *


@pytest.mark.parametrize(
    "email, expected",
    [
        ("test@example.com", True),
        ("invalid_email", False),
        ("test@test.example.com", True),
        ("test@example", False),
        ("test@example.", False),
    ],
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected


def test_random_date():
    # Define the age range
    start_age = 20
    end_age = 30

    # Calculate expected date range
    today = datetime.date.today()
    expected_end_date = today - datetime.timedelta(days=end_age * 365)
    expected_start_date = today - datetime.timedelta(days=start_age * 365)

    # Generate a random date
    generated_date = random_date(start_age, end_age)

    # Check if the generated date is in the correct format
    assert isinstance(generated_date, str)
    assert datetime.datetime.strptime(generated_date, "%Y-%m-%d")

    # Check if the generated date is within the expected range
    generated_date_obj = datetime.datetime.strptime(generated_date, "%Y-%m-%d").date()
    assert expected_end_date <= generated_date_obj <= expected_start_date


def test_generate_passport_data():
    # Define test data
    passport_number = "AB123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    # Call the method to generate passport data
    passport_data = generate_passport_data(
        passport_number, full_name, date_of_birth, blood_type
    )

    # Assert that the passport_data is a dictionary
    assert isinstance(passport_data, dict)

    # Assert that all keys are present in the returned dictionary
    expected_keys = [
        "number",
        "full_name",
        "place_of_birth",
        "date_of_birth",
        "date_of_issue",
        "date_of_expiry",
        "issuing_authority",
        "blood_type",
    ]
    assert all(key in passport_data for key in expected_keys)

    # Assert that the values are of the correct types
    assert isinstance(passport_data["number"], str)
    assert isinstance(passport_data["full_name"], str)
    assert isinstance(passport_data["place_of_birth"], str)
    assert isinstance(passport_data["date_of_birth"], str)
    assert isinstance(passport_data["date_of_issue"], str)
    assert isinstance(passport_data["date_of_expiry"], str)
    assert isinstance(passport_data["issuing_authority"], str)
    assert isinstance(passport_data["blood_type"], str)


def test_generate_driver_license_data():
    # Define test data
    driver_license_number = "DL123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    # Call the method to generate driver's license data
    driver_license_data = generate_driver_license_data(
        driver_license_number, full_name, date_of_birth, blood_type
    )

    # Assert that the driver_license_data is a dictionary
    assert isinstance(driver_license_data, dict)

    # Assert that all keys are present in the returned dictionary
    expected_keys = [
        "number",
        "full_name",
        "date_of_birth",
        "date_of_issue",
        "date_of_expiry",
        "sex",
        "blood_type",
        "weight",
    ]
    assert all(key in driver_license_data for key in expected_keys)

    # Assert that the values are of the correct types
    assert isinstance(driver_license_data["number"], str)
    assert isinstance(driver_license_data["full_name"], str)
    assert isinstance(driver_license_data["date_of_birth"], str)
    assert isinstance(driver_license_data["date_of_issue"], str)
    assert isinstance(driver_license_data["date_of_expiry"], str)
    assert isinstance(driver_license_data["sex"], str)
    assert isinstance(driver_license_data["blood_type"], str)
    assert isinstance(driver_license_data["weight"], int)

    # Assert that sex is either 'Male' or 'Female'
    assert driver_license_data["sex"] in ["Male", "Female"]

    # Assert that weight is within the specified range
    assert 50 <= driver_license_data["weight"] <= 100


def test_generate_health_card_data():
    # Define test data
    health_card_number = "HC123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    # Call the method to generate health card data
    health_card_data = generate_health_card_data(
        health_card_number, full_name, date_of_birth, blood_type
    )

    # Assert that the health_card_data is a dictionary
    assert isinstance(health_card_data, dict)

    # Assert that all keys are present in the returned dictionary
    expected_keys = [
        "number",
        "full_name",
        "date_of_birth",
        "date_of_issue",
        "insurance_provider",
        "policy_number",
        "blood_type",
        "covid_vaccination_status",
    ]
    assert all(key in health_card_data for key in expected_keys)

    # Assert that the values are of the correct types
    assert isinstance(health_card_data["number"], str)
    assert isinstance(health_card_data["full_name"], str)
    assert isinstance(health_card_data["date_of_birth"], str)
    assert isinstance(health_card_data["date_of_issue"], str)
    assert isinstance(health_card_data["insurance_provider"], str)
    assert isinstance(health_card_data["policy_number"], int)
    assert isinstance(health_card_data["blood_type"], str)
    assert isinstance(health_card_data["covid_vaccination_status"], str)

    # Assert that covid_vaccination_status is one of the specified values
    assert health_card_data["covid_vaccination_status"] in [
        "Fully Vaccinated",
        "Partially Vaccinated",
        "Not Vaccinated",
    ]


def test_generate_random_document_data():
    # Define test data
    full_name = "John Doe"
    passport_number = "AB123456"
    driver_license_number = "DL123456"
    health_card_number = "HC123456"

    # Call the method to generate random document data
    random_document_data = generate_random_document_data(
        full_name, passport_number, driver_license_number, health_card_number
    )

    # Assert that the random_document_data is a dictionary
    assert isinstance(random_document_data, dict)

    # Assert that the random_document_data contains the expected keys
    expected_keys = ["passport", "driver_license", "health_card"]
    assert all(key in random_document_data for key in expected_keys)

    # Assert that the values of each document are dictionaries
    for doc_data in random_document_data.values():
        assert isinstance(doc_data, dict)

    # Define expected keys for each document type
    expected_passport_keys = [
        "number",
        "full_name",
        "place_of_birth",
        "date_of_birth",
        "date_of_issue",
        "date_of_expiry",
        "issuing_authority",
        "blood_type",
    ]
    expected_driver_license_keys = [
        "number",
        "full_name",
        "date_of_birth",
        "date_of_issue",
        "date_of_expiry",
        "sex",
        "blood_type",
        "weight",
    ]
    expected_health_card_keys = [
        "number",
        "full_name",
        "date_of_birth",
        "date_of_issue",
        "insurance_provider",
        "policy_number",
        "blood_type",
        "covid_vaccination_status",
    ]

    # Assert that each document data contains the expected keys
    assert all(
        key in random_document_data["passport"] for key in expected_passport_keys
    )
    assert all(
        key in random_document_data["driver_license"]
        for key in expected_driver_license_keys
    )


def test_generate_random_bills_data():
    # Define test data
    account_id = "123456"

    # Call the method to generate random bills data
    bills_data = generate_random_bills_data(account_id)

    # Assert that the bills_data is a dictionary
    assert isinstance(bills_data, dict)

    # Assert that all keys are present in the returned dictionary
    expected_keys = [
        "user_id",
        "electricity",
        "internet_and_cable",
        "property_tax",
        "license",
        "registration",
    ]
    assert all(key in bills_data for key in expected_keys)

    # Assert that the values are of the correct types
    assert isinstance(bills_data["user_id"], str)
    assert isinstance(bills_data["electricity"], dict)
    assert isinstance(bills_data["internet_and_cable"], dict)
    assert isinstance(bills_data["property_tax"], dict)
    assert isinstance(bills_data["license"], dict)
    assert isinstance(bills_data["registration"], dict)

    # Assert that the electricity data contains the expected keys
    expected_electricity_keys = ["number", "due", "issued", "amount", "is_paid"]
    assert all(key in bills_data["electricity"] for key in expected_electricity_keys)

    # Assert that the internet_and_cable data contains the expected keys
    expected_internet_and_cable_keys = ["number", "due", "issued", "amount", "is_paid"]
    assert all(
        key in bills_data["internet_and_cable"]
        for key in expected_internet_and_cable_keys
    )

    # Assert that the property_tax data contains the expected keys
    expected_property_tax_keys = [
        "number",
        "issued",
        "due",
        "tax_rate",
        "value",
        "is_paid",
    ]
    assert all(key in bills_data["property_tax"] for key in expected_property_tax_keys)

    # Assert that the license data contains the expected keys
    expected_license_keys = [
        "number",
        "is_paid",
        "expiry_date",
        "renewal_fee",
        "renewal_period",
        "renewal_deadline",
    ]
    assert all(key in bills_data["license"] for key in expected_license_keys)

    # Assert that the registration data contains the expected keys
    expected_registration_keys = [
        "number",
        "is_paid",
        "make",
        "year",
        "plate_number",
        "expiry_date",
        "renewal_fee",
        "renewal_period",
        "renewal_deadline",
    ]
    assert all(key in bills_data["registration"] for key in expected_registration_keys)
