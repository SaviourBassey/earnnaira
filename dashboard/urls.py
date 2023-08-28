from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("my-accounts/", views.MyAccountView.as_view(), name="my_accounts_view"),
    path("my-referrals/", views.ReferralView.as_view(), name="my_referrals_view"),
    path("payments-request/", views.RequestPaymentView.as_view(), name="request_payment_view"),
]
