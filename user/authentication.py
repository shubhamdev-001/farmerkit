
import uuid
import jwt
from django.core.mail import EmailMessage,send_mail
from rest_framework import status
from rest_framework.response import Response
import random
import string
from datetime import *
from django.contrib.auth.hashers import check_password
from .models import *
from django.conf import settings  # SECRET_KEY from settings.py
from farmerkit.settings import *
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


# def checkIfUserAuthenticated(request, model, serializer_class):
#     # Check if the Authorization header is present
#     if "Authorization" in request.headers:
#         auth_header = request.headers["Authorization"]

#         # Check if the header starts with 'Bearer '
#         if auth_header.startswith("Bearer "):
#             token = auth_header.replace("Bearer ", "")
#             try:
#                 # Decode the JWT token
#                 decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                
#                 # Retrieve user instance by decoded ID
#                 user_instance = model.objects.filter(id=decoded['id']).first()

#                 if user_instance is None:
#                     return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#                 # Serialize the user data
#                 serializer = serializer_class(user_instance)
#                 return Response(serializer.data)

#             except jwt.ExpiredSignatureError:
#                 return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
#             except jwt.InvalidTokenError:
#                 return Response({"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

#         else:
#             return Response({"message": "Authorization header must start with 'Bearer '"}, status=status.HTTP_401_UNAUTHORIZED)

#     else:
#         return Response({"message": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
    
# def checkIfUserAuthenticated(request, model, serializer):
#     print(request)
#     if ("Authorization" in request.headers):
#         authorization = request.headers['Authorization']
#         if ("Bearer" in authorization):
#             jwtP = authorization.replace("Bearer ", "")
#             try:
#                 decoded = jwt.decode(
#                     jwtP,  SECRET_KEY, algorithms=["HS256"])
#                 queryset = model.objects.filter(
#                     id=decoded['id']).first()
#                 print(queryset)
#                 if (queryset is None):
#                     return Response("Not found", status=status.HTTP_404_NOT_FOUND)
#                 serializer = serializer(queryset, many=False)

#                 return Response(serializer.data)
#             except:
#                 return Response({"message": "Token is invalid", "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({"message": "Token is invalid", "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         return Response({"message": "Unauthorized access.", "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
    
# def emailAuthentication(email, password, model):
#     user = model.objects.filter(email=email).first()
#     if (user is None):
#         return Response({"message": "User not found", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

#     is_authenticated = check_password(password, user.password)
#     if (is_authenticated):
#         jwt_token = jwt.encode(
#             {'email': user.email, 'id': user.id, 'secret_token': str(uuid.uuid4())}, SECRET_KEY, algorithm="HS256")
#         return Response({'access': jwt_token})
#     else:
#         return Response({"message": "Invalid credentials", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_401_UNAUTHORIZED)

    




def checkIfUserAuthenticated(request, model, serializer):
    if "Authorization" in request.headers:
        authorization = request.headers["Authorization"]
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "").strip()
            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = model.objects.filter(id=decoded.get("id")).first()

                if not user:
                    return Response("User not found", status=status.HTTP_404_NOT_FOUND)

                return Response(serializer(user).data)

            except ExpiredSignatureError:
                return Response({"message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except InvalidTokenError as e:
                return Response({"message": f"Invalid token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)

def emailAuthentication(email, password, model):
    user = model.objects.filter(email=email).first()
    if user is None:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if check_password(password, user.password):
        payload = {
            'id': user.id,
            'email': user.email,
            'secret_token': str(uuid.uuid4()),
             'iat': datetime.now(),
            'exp': datetime.now() + timedelta(hours=2),        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return Response({'access': jwt_token})
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

# def generate_otp(length=4):
#     """Generate a 6-digit OTP"""
#     return ''.join(random.choices(string.digits, k=length))



# def store_otp(email, otp):
#     """Store OTP in the database with a 5-minute expiration"""
#     OTP.objects.update_or_create(
#         email=email,
#         defaults={"otp": otp, "expires_at": now() + timedelta(minutes=5)}
#     )

# def validate_otp(email, otp):
#     """Verify OTP from the database"""
#     try:
#         otp_entry = OTP.objects.get(email=email)
#         if otp_entry.is_valid() and otp_entry.otp == otp:
#             otp_entry.delete()
#             return True
#     except OTP.DoesNotExist:
#         return False
#     return False