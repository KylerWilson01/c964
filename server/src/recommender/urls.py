from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlPaths = [
    path("recommendations/", views.get_recommendations_for, name="get-recommendations"),
    path("ratings/", views.get_prev_ratings, name="get-ratings"),
    path("ratings/save/", views.save_rating, name="save-ratings"),
    path("register/", views.sign_up, name="register-user"),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = format_suffix_patterns(urlPaths)
