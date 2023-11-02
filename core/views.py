from django.http import HttpRequest, JsonResponse

from .egyptian_national_id import EgyptianNationalId


def index(_: HttpRequest, national_id: str) -> JsonResponse:
    try:
        national_id = EgyptianNationalId(national_id)
    except ValueError:
        return JsonResponse({"error": "Invalid national ID"}, status=400)

    return JsonResponse(national_id.fields)
