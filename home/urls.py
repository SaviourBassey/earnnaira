from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("about-earnnaira/", views.AboutView.as_view(), name="about_view"),
    path("top-earners/", views.TopEarnerView.as_view(), name="top_earners_view"),
]
