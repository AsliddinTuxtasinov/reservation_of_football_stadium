from django.contrib import admin

from accounts.models import User


# Registering the User model with the admin site
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # List of fields to display in the admin interface for User objects
    list_display = ["username", "email", "phone_number", "user_roles"]
