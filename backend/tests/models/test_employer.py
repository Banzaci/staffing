
import uuid

from app.models.employer import Employer
from app.models.business import Business
from app.models.business_type import BusinessType
from app.models.business_type_translation import BusinessTypeTranslation


def test_create_employer():
    user_id = uuid.uuid4()

    employer = Employer(user_id=user_id)

    assert employer.user_id == user_id
    assert employer.id is None


def test_create_business_type():
    business_type = BusinessType(code="restaurant")

    assert business_type.code == "restaurant"
    assert business_type.id is None
    


def test_create_business_type_translation():
    business_type_id = uuid.uuid4()

    translation = BusinessTypeTranslation(
        business_type_id=business_type_id,
        language_code="sv",
        name="Restaurang",
    )

    assert translation.business_type_id == business_type_id
    assert translation.language_code == "sv"
    assert translation.name == "Restaurang"


def test_create_business():
    employer_id = uuid.uuid4()
    business_type_id = uuid.uuid4()

    business = Business(
        employer_id=employer_id,
        name="Sunset Beach Resort",
        business_type_id=business_type_id,
        country_code="PH",
        latitude=9.7845,
        longitude=126.1589,
    )

    assert business.employer_id == employer_id
    assert business.country_code == "PH"
    assert business.name == "Sunset Beach Resort"
    assert business.business_type_id == business_type_id
    assert business.latitude == 9.7845
    assert business.longitude == 126.1589


def test_business_optional_location():
    business = Business(
        employer_id=uuid.uuid4(),
        name="Beach Restaurant",
        business_type_id=uuid.uuid4(),
    )

    assert business.latitude is None
    assert business.longitude is None
