import pytest
import datetime
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
    """
    Test the validity of email addresses.

    Args:
        email (str): The email address to test.
        expected (bool): The expected result of the validity check.

    Returns:
        None
    """
    assert is_valid_email(email) == expected


def test_random_date():
    """
    Test the generation of a random date within a specified age range.

    Returns:
        None
    """
    start_age = 20
    end_age = 30

    today = datetime.date.today()
    expected_end_date = today - datetime.timedelta(days=end_age * 365)
    expected_start_date = today - datetime.timedelta(days=start_age * 365)

    generated_date = random_date(start_age, end_age)

    assert isinstance(generated_date, str)
    assert datetime.datetime.strptime(generated_date, "%Y-%m-%d")

    generated_date_obj = datetime.datetime.strptime(generated_date, "%Y-%m-%d").date()
    assert expected_end_date <= generated_date_obj <= expected_start_date


def test_generate_passport_data():
    """
    Test the generation of passport data.

    Returns:
        None
    """
    passport_number = "AB123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    passport_data = generate_passport_data(
        passport_number, full_name, date_of_birth, blood_type
    )

    assert isinstance(passport_data, dict)

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

    assert isinstance(passport_data["number"], str)
    assert isinstance(passport_data["full_name"], str)
    assert isinstance(passport_data["place_of_birth"], str)
    assert isinstance(passport_data["date_of_birth"], str)
    assert isinstance(passport_data["date_of_issue"], str)
    assert isinstance(passport_data["date_of_expiry"], str)
    assert isinstance(passport_data["issuing_authority"], str)
    assert isinstance(passport_data["blood_type"], str)


def test_generate_driver_license_data():
    """
    Test the generation of driver's license data.

    Returns:
        None
    """
    driver_license_number = "DL123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    driver_license_data = generate_driver_license_data(
        driver_license_number, full_name, date_of_birth, blood_type
    )

    assert isinstance(driver_license_data, dict)

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

    assert isinstance(driver_license_data["number"], str)
    assert isinstance(driver_license_data["full_name"], str)
    assert isinstance(driver_license_data["date_of_birth"], str)
    assert isinstance(driver_license_data["date_of_issue"], str)
    assert isinstance(driver_license_data["date_of_expiry"], str)
    assert isinstance(driver_license_data["sex"], str)
    assert isinstance(driver_license_data["blood_type"], str)
    assert isinstance(driver_license_data["weight"], int)

    assert driver_license_data["sex"] in ["Male", "Female"]

    assert 50 <= driver_license_data["weight"] <= 100


def test_generate_health_card_data():
    """
    Test the generation of health card data.

    Returns:
        None
    """
    health_card_number = "HC123456"
    full_name = "John Doe"
    date_of_birth = "1990-01-01"
    blood_type = "O+"

    health_card_data = generate_health_card_data(
        health_card_number, full_name, date_of_birth, blood_type
    )

    assert isinstance(health_card_data, dict)

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

    assert isinstance(health_card_data["number"], str)
    assert isinstance(health_card_data["full_name"], str)
    assert isinstance(health_card_data["date_of_birth"], str)
    assert isinstance(health_card_data["date_of_issue"], str)
    assert isinstance(health_card_data["insurance_provider"], str)
    assert isinstance(health_card_data["policy_number"], int)
    assert isinstance(health_card_data["blood_type"], str)
    assert isinstance(health_card_data["covid_vaccination_status"], str)

    assert health_card_data["covid_vaccination_status"] in [
        "Fully Vaccinated",
        "Partially Vaccinated",
        "Not Vaccinated",
    ]


def test_generate_random_document_data():
    """
    Test the generation of random document data.

    Returns:
        None
    """
    full_name = "John Doe"
    passport_number = "AB123456"
    driver_license_number = "DL123456"
    health_card_number = "HC123456"

    random_document_data = generate_random_document_data(
        full_name, passport_number, driver_license_number, health_card_number
    )

    assert isinstance(random_document_data, dict)

    expected_keys = ["passport", "driver_license", "health_card"]
    assert all(key in random_document_data for key in expected_keys)

    for doc_data in random_document_data.values():
        assert isinstance(doc_data, dict)

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

    assert all(
        key in random_document_data["passport"] for key in expected_passport_keys
    )
    assert all(
        key in random_document_data["driver_license"]
        for key in expected_driver_license_keys
    )


def test_generate_random_bills_data():
    """
    Test the generation of random bills data.

    Returns:
        None
    """
    account_id = "123456"

    bills_data = generate_random_bills_data(account_id)

    assert isinstance(bills_data, dict)

    expected_keys = [
        "user_id",
        "electricity",
        "internet_and_cable",
        "property_tax",
        "license",
        "registration",
    ]
    assert all(key in bills_data for key in expected_keys)

    assert isinstance(bills_data["user_id"], str)
    assert isinstance(bills_data["electricity"], dict)
    assert isinstance(bills_data["internet_and_cable"], dict)
    assert isinstance(bills_data["property_tax"], dict)
    assert isinstance(bills_data["license"], dict)
    assert isinstance(bills_data["registration"], dict)

    expected_electricity_keys = ["number", "due", "issued", "amount", "is_paid"]
    assert all(key in bills_data["electricity"] for key in expected_electricity_keys)

    expected_internet_and_cable_keys = ["number", "due", "issued", "amount", "is_paid"]
    assert all(
        key in bills_data["internet_and_cable"]
        for key in expected_internet_and_cable_keys
    )

    expected_property_tax_keys = [
        "number",
        "issued",
        "due",
        "tax_rate",
        "value",
        "is_paid",
    ]
    assert all(key in bills_data["property_tax"] for key in expected_property_tax_keys)

    expected_license_keys = [
        "number",
        "is_paid",
        "expiry_date",
        "renewal_fee",
        "renewal_period",
        "renewal_deadline",
    ]
    assert all(key in bills_data["license"] for key in expected_license_keys)

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
