from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "user_roles", "email", "phone_number"]


class LoginSerializers(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Validate user input and authenticate user
        user = self.auth_validate(attrs=attrs)
        data = user.token()

        # Update last login if configured
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data

    def auth_validate(self, attrs):
        # Extract user input and password from attributes
        password = str(attrs.get("password"))
        username = str(attrs.get("username"))

        # Retrieve user based on authentication type
        user = self.get_user(username=username)

        # Authenticate user using username and password
        user = authenticate(username=user.username, password=password)

        # Handle incorrect login credentials
        if user is not None:
            return user
        else:
            raise exceptions.ValidationError(detail={
                "success": False,
                "err_msg": "Sorry, the login or password you entered is incorrect. Please check and try again!"
            })

    @staticmethod
    def get_user(**kwargs):
        # Retrieve user from the database based on provided kwargs
        user_queryset = User.objects.filter(**kwargs)
        user = user_queryset.first()

        # Handle no active account found
        if user is None:
            raise exceptions.ValidationError(detail={
                "success": True,
                "err_msg": "No active account found!"
            })

        return user
