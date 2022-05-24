from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from . import views

urlpatterns = [
    path('register/', views.SignupView.as_view(), name='register'),
    path('token/', obtain_jwt_token),  # 토큰 발급
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),  # 인증
]