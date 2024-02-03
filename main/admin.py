from django.contrib import admin

from main.models import Stadiums, StadiumsPictures, StadiumsBooked


class StadiumsPicturesAdminInline(admin.TabularInline):
    model = StadiumsPictures
    extra = 0  # Number of empty forms to display
    fields = ["stadium", "image"]


@admin.register(Stadiums)
class StadiumsAdmin(admin.ModelAdmin):
    list_display = ["name", "per_address", "price"]
    search_fields = ["name", "per_address"]
    inlines = [StadiumsPicturesAdminInline]


@admin.register(StadiumsBooked)
class StadiumsBookedAdmin(admin.ModelAdmin):
    list_display = ["client", "stadium", "starts_time", "ends_time", "is_busy_now"]
