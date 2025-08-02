from rest_framework.permissions import BasePermission
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from .models import *
from .authentication import *
from .serializer import *

class IsAuthenticated(BasePermission):
    """Custom permission to check if the user is an authenticated customer."""
    
    def has_permission(self, request, view):
        response = checkIfUserAuthenticated(request, User, AuthUserSerializer)

        if response.status_code == 200:
            user_data = response.data
            user_id = user_data.get("id")
            if not user_id:
                raise NotAuthenticated("Authentication failed: User ID not found.")

            user = User.objects.filter(id=user_id, is_active=True).first()
            if not user:
                raise NotAuthenticated("User not found or inactive.")
            request.user = user 
            return True

        raise NotAuthenticated("You are not authenticated to access this resource.")
    

