from typing import Any, List
import uuid
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *
from .permissions import *
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .utils import generate_otp, send_otp_email
from django.utils.timezone import now


class UserAddViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [AllowAny]

# -------------------------------------------APIVIEWS-------------------------------------------


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProtectedUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializers(user)
        return Response({
            "message": "Access granted",
            "user": serializer.data
        })




class SendOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=400)

            otp = generate_otp()
            OTP.objects.create(user=user, otp_code=otp)
            send_otp_email(user.email, otp)
            return Response({"message": "OTP sent successfully."})
        return Response(serializer.errors, status=400)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_entry = OTP.objects.filter(user=user, otp_code=otp, is_verified=False).latest('created_at')
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({"error": "Invalid OTP."}, status=400)

            # Check if OTP is expired (valid for 10 minutes)
            if  now() - otp_entry.created_at > timedelta(minutes=5):
                return Response({"error": "OTP expired."}, status=400)

            otp_entry.is_verified = True
            otp_entry.save()
            return Response({"message": "OTP verified successfully."})
        return Response(serializer.errors, status=400)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                otp_entry = OTP.objects.filter(user=user, is_verified=True).latest('created_at')
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({"error": "OTP verification required."}, status=400)

            user.set_password(new_password)
            user.save()
            otp_entry.delete()  # cleanup
            return Response({"message": "Password reset successful."})
        return Response(serializer.errors, status=400)

