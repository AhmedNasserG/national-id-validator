from datetime import datetime
from django.test import SimpleTestCase
import time_machine

from .egyptian_national_id import EgyptianNationalId
from .exceptions import InvalidNationalIdException



class ValidEgyptianNationalIdTestCase(SimpleTestCase):
    VALID_NATIONAL_ID = "30107211500852"

    @classmethod
    def setUpClass(cls) -> None:
        cls.national_id = EgyptianNationalId(cls.VALID_NATIONAL_ID)

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


class InvalidEgyptianNationalIdTestCase(SimpleTestCase):
    def test_national_id_with_invalid_century(self):
        """
        Test invalid national ID with invalid century.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("10107211500852")

    def test_national_id_with_invalid_month(self):
        """
        Test invalid national ID with invalid year.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("30100211500852")

    def test_national_id_with_invalid_day(self):
        """
        Test invalid national ID with invalid day.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("30107411500852")

    @time_machine.travel(datetime(2010, 1, 1, 0, 0))
    def test_national_id_with_birth_date_in_future(self):
        """
        Test invalid national ID with birth date in future.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("31107211500852")

    def test_national_id_with_invalid_governorate_code(self):
        """
        Test invalid national ID with invalid governorate code.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("30107210500852")

    def test_national_id_with_invalid_gender_code(self):
        """
        Test invalid national ID with invalid gender code.
        """
        with self.assertRaises(InvalidNationalIdException):
            EgyptianNationalId("30107211500802")
