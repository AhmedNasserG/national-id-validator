import re
from datetime import datetime

EGYPTIAN_NATIONAL_ID_REGEX = (
    r"^(2|3)"  # birth century
    r"([0-9]{2})"  # birth year
    r"(0[1-9]|1[0-2])"  # birth month
    r"(0[1-9]|1[0-9]|2[0-9]|3[0-1])"  # birth day
    # governorate code
    r"(01|02|03|04|11|12|13|14|15|16|17|18|19|21|22|23|24|25|26|27|28|29|31|32|33|34|35|88)"
    r"(\d{3})"  # sequence number
    r"([1-9])"  # gender
    r"(\d)$"  # verification digit
)

BIRTH_CENTURY_INDEX = 1
BIRTH_YEAR_INDEX = 2
BIRTH_MONTH_INDEX = 3
BIRTH_DAY_INDEX = 4
GOVERNORATE_CODE_INDEX = 5
SEQUENCE_NUMBER_INDEX = 6
GENDER_CODE_INDEX = 7
VERIFICATION_DIGIT_INDEX = 8

CENTURIES: dict[str, int] = {"2": 1900, "3": 2000}

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

        self.fields["birth_date"] = self.__parse_birth_date(
            match[BIRTH_CENTURY_INDEX],
            match[BIRTH_YEAR_INDEX],
            match[BIRTH_MONTH_INDEX],
            match[BIRTH_DAY_INDEX],
        )
        self.fields["governorate"] = self.__parse_governorate(
            match[GOVERNORATE_CODE_INDEX]
        )
        self.fields["gender"] = self.__parse_gender(match[GENDER_CODE_INDEX])

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
        return datetime(birth_year, birth_month, birth_day).date()

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
