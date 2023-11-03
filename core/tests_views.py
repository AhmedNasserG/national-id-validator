from django.test import SimpleTestCase
from parameterized import parameterized
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class NationalIdValidatorTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    @parameterized.expand(
        [
            [
                "30107211500852",
                status.HTTP_200_OK,
                {
                    "birth_date": "2001-07-21",
                    "governorate": "Kafr El - Sheikh",
                    "gender": "MALE",
                },
            ],
            [
                "12345678901234",
                status.HTTP_400_BAD_REQUEST,
                {"error": "Invalid national ID"},
            ],
            [
                "INVALID_VALUE",
                status.HTTP_400_BAD_REQUEST,
                {"error": "Invalid national ID"},
            ],
        ]
    )
    def test_valid_national_id(
        self, national_id, expected_status_code, expected_response
    ):
        url = reverse("national_id", args=[national_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(
            response.json(),
            expected_response,
        )
