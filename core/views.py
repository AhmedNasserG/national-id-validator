from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .egyptian_national_id import EgyptianNationalId
from .exceptions import InvalidNationalIdException


@swagger_auto_schema(
    method="get",
    operation_summary="Validate Egyptian National ID",
    operation_description="Validates an Egyptian National ID and returns its fields",
    responses={
        200: openapi.Response(
            "Successful Response",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "birth_date": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The birth date of the ID holder in the format YYYY-MM-DD",
                    ),
                    "governorate": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The governorate of the ID holder",
                    ),
                    "gender": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The gender of the ID holder (MALE or FEMALE)",
                    ),
                },
            ),
        ),
        400: openapi.Response(
            "Invalid national ID",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Invalid national ID"
                    ),
                },
            ),
        ),
    },
)
@api_view(["GET"])
def index(_: HttpRequest, national_id: str) -> JsonResponse:
    try:
        national_id = EgyptianNationalId(national_id)
    except InvalidNationalIdException as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(national_id.fields)
