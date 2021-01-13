from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    SessionCreateView,
    TransactionValidationView,
)


app_name = "myapp"

urlpatterns = [
    path("session", csrf_exempt(SessionCreateView.as_view())),
    path("validate", csrf_exempt(TransactionValidationView.as_view())),
]
