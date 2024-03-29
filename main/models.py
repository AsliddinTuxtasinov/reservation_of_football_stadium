from django.db import models
from django.utils import timezone

from accounts.enums import AccountRoleEnums
from accounts.models import User
from config.abstract_models import BaseModel
from main.utils import slugify_upload


class Stadiums(BaseModel):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="stadiums",
        limit_choices_to={
            "user_roles": AccountRoleEnums.STADIUM_OWNER
        }
    )

    name = models.CharField(max_length=255)
    per_address = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)  # sum
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def get_all_stadium_pictures(self):
        return self.images.all()

    def get_all_booked_objs(self):
        return self.stadiums_booked.all()

    def __str__(self):
        return f"{self.name}({self.per_address})"

    class Meta:
        db_table = 'stadiums'


class StadiumsPictures(BaseModel):
    stadium = models.ForeignKey(to=Stadiums, on_delete=models.CharField, related_name="images")
    image = models.ImageField(upload_to=slugify_upload)

    def __str__(self):
        return f"{self.stadium.name} (picture): {self.id}"

    class Meta:
        db_table = 'stadium_pictures'


class StadiumsBooked(BaseModel):
    client = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="client_booked",
        limit_choices_to={
            "user_roles": AccountRoleEnums.USER
        }
    )

    stadium = models.ForeignKey(
        to=Stadiums,
        on_delete=models.CASCADE,
        related_name="stadiums_booked",
    )
    starts_time = models.DateTimeField()
    ends_time = models.DateTimeField()

    @property
    def is_busy_now(self):
        current_time = timezone.now()
        return self.starts_time <= current_time <= self.ends_time

    def __str__(self):
        return f"{self.stadium.name} (starts_time: {self.starts_time}, ends_time: {self.ends_time})"

    class Meta:
        db_table = 'stadiums_booked'
