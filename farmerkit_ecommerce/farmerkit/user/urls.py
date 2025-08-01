from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()

router.register(r"register", UserAddViewSet, basename="customer-register")


urlpatterns = router.urls + [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/user-profile/', ProtectedUserView.as_view(), name='user-profile'),
    path('api/send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]