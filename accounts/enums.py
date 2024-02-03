from django.db.models import enums


class AccountRoleEnums(enums.TextChoices):
    ADMIN = "admin", "admin"
    STADIUM_OWNER = "stadium owner", "stadium owner"
    USER = "user", "user"
