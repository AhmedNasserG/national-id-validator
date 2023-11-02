from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from .egyptian_national_id import EgyptianNationalId


class ValidEgyptianNationalIdTestCase(TestCase):
    VALID_NATIONAL_ID = "30107211500852"

    def setUp(self) -> None:
        self.national_id = EgyptianNationalId(self.VALID_NATIONAL_ID)

    def test_birth_date(self):
        """
        Test birth date parsing.
        """
        self.assertEqual(
            self.national_id.fields["birth_date"], datetime(2001, 7, 21).date()
        )

    def test_governorate(self):
        """
        Test governorate parsing.
        """
        self.assertEqual(self.national_id.fields["governorate"], "Kafr El - Sheikh")

    def test_gender(self):
        """
        Test gender parsing
        """
        self.assertEqual(self.national_id.fields["gender"], "MALE")


class InvalidEgyptianNationalIdTestCase(TestCase):
    def test_national_id_with_invalid_century(self):
        """
        Test invalid national ID with invalid century.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("10107211500852")

    def test_national_id_with_invalid_month(self):
        """
        Test invalid national ID with invalid year.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("30100211500852")

    def test_national_id_with_invalid_day(self):
        """
        Test invalid national ID with invalid day.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("30107411500852")

    @freeze_time("2010-01-01")
    def test_national_id_with_birth_date_in_future(self):
        """
        Test invalid national ID with birth date in future.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("31107211500852")

    def test_national_id_with_invalid_governorate_code(self):
        """
        Test invalid national ID with invalid governorate code.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("30107210500852")

    def test_national_id_with_invalid_gender_code(self):
        """
        Test invalid national ID with invalid gender code.
        """
        with self.assertRaises(ValueError):
            EgyptianNationalId("30107211500802")


class NationalIdValidatorTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_national_id(self):
        url = reverse("national_id", args=["30107211500852"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "birth_date": "2001-07-21",
                "governorate": "Kafr El - Sheikh",
                "gender": "MALE",
            },
        )

    def test_invalid_national_id(self):
        url = reverse("national_id", args=["12345678901234"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Invalid national ID"})
