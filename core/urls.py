from django.urls import path
from . import views


urlpatterns = [
    path("national-id/<str:national_id>/", views.index, name="national_id"),
]
