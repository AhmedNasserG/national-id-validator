import re
from datetime import datetime


BIRTH_CENTURY = "birth_century"
BIRTH_YEAR = "birth_year"
BIRTH_MONTH = "birth_month"
BIRTH_DAY = "birth_day"
GOVERNORATE_CODE = "governorate_code"
SEQUENCE_NUMBER = "sequence_number"
GENDER_CODE = "gender_code"
VERIFICATION_DIGIT = "verification_digit"

BIRTH_DATE_FIELD = "birth_date"
GOVERNORATE_FIELD = "governorate"
GENDER_FIELD = "gender"

GOVERNORATES: dict[str, str] = {
    "01": "Cairo",
    "02": "Alexandria",
    "03": "Port Said",
    "04": "Suez",
    "11": "Damietta",
    "12": "Dakahlia",
    "13": "Ash Sharqia",
    "14": "Kaliobeya",
    "15": "Kafr El - Sheikh",
    "16": "Gharbia",
    "17": "Monoufia",
    "18": "El Beheira",
    "19": "Ismailia",
    "21": "Giza",
    "22": "Beni Suef",
    "23": "Fayoum",
    "24": "El Menia",
    "25": "Assiut",
    "26": "Sohag",
    "27": "Qena",
    "28": "Aswan",
    "29": "Luxor",
    "31": "Red Sea",
    "32": "New Valley",
    "33": "Matrouh",
    "34": "North Sinai",
    "35": "South Sinai",
    "88": "Foreign",
}

CENTURIES: dict[str, int] = {"2": 1900, "3": 2000}

EGYPTIAN_NATIONAL_ID_REGEX = (
    rf"^(?P<{BIRTH_CENTURY}>{'|'.join(CENTURIES.keys())})"
    rf"(?P<{BIRTH_YEAR}>[0-9]{{2}})"
    rf"(?P<{BIRTH_MONTH}>0[1-9]|1[0-2])"
    rf"(?P<{BIRTH_DAY}>0[1-9]|1[0-9]|2[0-9]|3[0-1])"
    rf"(?P<{GOVERNORATE_CODE}>{'|'.join(GOVERNORATES.keys())})"
    rf"(?P<{SEQUENCE_NUMBER}>\d{{3}})"
    rf"(?P<{GENDER_CODE}>[1-9])"
    rf"(?P<{VERIFICATION_DIGIT}>\d)$"
)


class EgyptianNationalId:
    """
    Egyptian national ID class.
    """

    def __init__(self, national_id: str):
        self.national_id = national_id
        self.fields = {}

        if not self.__is_valid(self.national_id):
            raise ValueError("Invalid national ID")

        match = re.match(EGYPTIAN_NATIONAL_ID_REGEX, self.national_id)

        self.fields[BIRTH_DATE_FIELD] = self.__parse_birth_date(
            match[BIRTH_CENTURY],
            match[BIRTH_YEAR],
            match[BIRTH_MONTH],
            match[BIRTH_DAY],
        )
        self.fields[GOVERNORATE_FIELD] = self.__parse_governorate(
            match[GOVERNORATE_CODE]
        )
        self.fields[GENDER_FIELD] = self.__parse_gender(match[GENDER_CODE])

    def __is_valid(self, national_id: str) -> bool:
        """
        Check if the national ID is valid or not.
        """
        match = re.match(EGYPTIAN_NATIONAL_ID_REGEX, national_id)
        return bool(match)

    def __parse_birth_date(
        self, century: str, year: str, month: str, day: str
    ) -> datetime.date:
        """
        Parse birth date from national ID.
        """
        birth_year = CENTURIES[century] + int(year)
        birth_month = int(month)
        birth_day = int(day)
        birth_date = datetime(birth_year, birth_month, birth_day).date()

        if birth_date > datetime.now().date():
            raise ValueError("Invalid birth date")

        return birth_date

    def __parse_governorate(self, governorate_code: str) -> str:
        """
        Parse governorate from national ID.
        """
        return GOVERNORATES[governorate_code]

    def __parse_gender(self, gender_code: str) -> str:
        """
        Parse gender from national ID.
        """
        return "MALE" if int(gender_code) % 2 == 1 else "FEMALE"
