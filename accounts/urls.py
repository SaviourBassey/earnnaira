from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="register_view"),
    path("login/", views.SignInView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("online-vendors/", views.VendorView.as_view(), name="vendor_view"),
]
