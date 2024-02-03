import random
import uuid

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.enums import AccountRoleEnums
from config.abstract_models import BaseModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    user_roles = models.CharField(max_length=35, choices=AccountRoleEnums.choices, default=AccountRoleEnums.USER)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def check_username(self):
        if not self.username:
            temp_username = f"{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"

            self.username = temp_username

    def check_email(self):
        if not self.email:
            normalize_email = str(self.email).lower()  # Asliddin@gmail.com -> asliddin@gmail.com
            self.email = normalize_email

    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "full_name": self.full_name,
            "user_roles": self.user_roles,
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def clean(self):
        self.check_username()
        self.check_email()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
