from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("earnnaira-posts/", views.BlogHomeView.as_view(), name="blog_home_view"),
    path("<slug:SLUG>/<int:ID>", views.PostDetailView.as_view(), name="blog_detail_view"),
]
