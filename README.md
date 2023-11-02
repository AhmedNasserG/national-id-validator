# national-id-validator

![test workflow](https://github.com/AhmedNasserG/national-id-validator/actions/workflows/test.yml/badge.svg)
![linter workflow](https://github.com/AhmedNasserG/national-id-validator/actions/workflows/test.yml/badge.svg)

A simple API for validating and extracting key information from Egyptian National ID numbers

## Project Setup

```bash
git clone git@github.com:AhmedNasserG/national-id-validator.git
cd national-id-validator
pip install poetry
poetry install
poetry run python manage.py runserver
```

## Project Testing

### Unit tests

```bash
poetry run python manage.py tests
```

### Consume the api from the terminal

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/national-id/{national-id}/'
```

### Consume the api from swagger

go to `http://127.0.0.1:8000/swagger/` to find the documentation and use `Try it out` option

## API Documentations

### Swagger

`http://127.0.0.1:8000/swagger/`

### Redoc

`http://127.0.0.1:8000/redoc/`

### Examples

#### 1. Successful example

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/national-id/30107211500852/'
```

**Response**

```json
{
  "birth_date": "2001-07-21",
  "governorate": "Kafr El - Sheikh",
  "gender": "MALE"
}
```

---

#### 1. failure example

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/national-id/10207231500852/'
```

**Response**

```json
{
  "error": "Invalid national ID"
}
```

## Background information regarding id parsing

- Egyptian national id is 14 digit
- The id can be splitted to the following form `c - yymmdd - ss - iiig - z` where
  - `c` is the birth century (2 represent 1900 to 1999, 3 represent 2000 to 2099 .. etc)
  - `yymmdd` is the date of birth
  - `ss` is the birth governorate code (88 for people who born in a foreign country, 01 for who born in Cairo, ...etc )
  - `iiig` is the sequence in the computer between births in this birthday
  - `g` represents the gender (2,4,6,8 for females and 1,3,5,7,9)
  - `z` is a number Ministry of Interior added it to validate if the National ID fake or not (1 to 9)

<details>
  <summary>The governorate codes</summary>

| Governorate Code | Governorate      |
| ---------------- | ---------------- |
| 01               | Cairo            |
| 02               | Alexandria       |
| 03               | Port Said        |
| 04               | Suez             |
| 11               | Damietta         |
| 12               | Dakahlia         |
| 13               | Ash Sharqia      |
| 14               | Kaliobeya        |
| 15               | Kafr El - Sheikh |
| 16               | Gharbia          |
| 17               | Monoufia         |
| 18               | El Beheira       |
| 19               | Ismailia         |
| 21               | Giza             |
| 22               | Beni Suef        |
| 23               | Fayoum           |
| 24               | El Menia         |
| 25               | Assiut           |
| 26               | Sohag            |
| 27               | Qena             |
| 28               | Aswan            |
| 29               | Luxor            |
| 31               | Red Sea          |
| 32               | New Valley       |
| 33               | Matrouh          |
| 34               | North Sinai      |
| 35               | South Sinai      |
| 88               | Foreign          |

</details>

Credits for the background information [stackexchange](https://codereview.stackexchange.com/questions/221899/extract-information-from-egyptian-national-id)

## License

MIT License © 2023 Ahmed Nasser
