from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("my-accounts/", views.MyAccountView.as_view(), name="my_accounts_view"),
]
