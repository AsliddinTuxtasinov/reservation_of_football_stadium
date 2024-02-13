from rest_framework import serializers

from accounts.seializers import UserSerializers
from main.models import Stadiums, StadiumsBooked, StadiumsPictures
from main.utils import haversine


class StadiumsListCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stadiums
        fields = ['id', 'name', 'per_address', 'contact_phone_number', 'price', 'latitude', 'longitude']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["stadium_owner"] = UserSerializers(instance.owner).data
        return rep


class StadiumsListForUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stadiums
        fields = ['id', 'name', 'per_address', 'contact_phone_number', 'price', 'latitude', 'longitude']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["stadium_owner"] = UserSerializers(instance.owner).data

        latitude = self.context.get("latitude")
        longitude = self.context.get("longitude")

        if latitude and longitude:
            rep["distance"] = haversine(
                lat1=latitude, lon1=longitude, lat2=instance.latitude, lon2=instance.longitude
            )
        return rep


# class StadiumsListForUserFilterSerializers(serializers.Serializer):
#     latitude = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=True, required=False)
#     longitude = serializers.DecimalField(max_digits=9, decimal_places=6, allow_null=True, required=False)
#
#     starts_time = serializers.DateTimeField(allow_null=True, required=False)
#     ends_time = serializers.DateTimeField(allow_null=True, required=False)
#
#     def validate(self, attrs):
#         latitude = attrs.get("latitude")
#         longitude = attrs.get("longitude")
#
#         starts_time = attrs.get("starts_time")
#         ends_time = attrs.get("ends_time")
#
#         # Check if latitude is not None and longitude is None
#         if latitude is not None and longitude is None:
#             raise serializers.ValidationError("If latitude is provided, longitude must also be provided.")
#
#         # Check if latitude is not None and longitude is None
#         if longitude is not None and latitude is None:
#             raise serializers.ValidationError("If latitude is provided, longitude must also be provided.")
#
#         # Check if latitude is not None and longitude is None
#         if starts_time is not None and ends_time is None:
#             raise serializers.ValidationError("If starts_time is provided, ends_time must also be provided.")
#
#         # Check if latitude is not None and longitude is None
#         if ends_time is not None and starts_time is None:
#             raise serializers.ValidationError("If starts_time is provided, ends_time must also be provided.")
#
#         return attrs


class StadiumsPicturesSerializers(serializers.ModelSerializer):
    class Meta:
        model = StadiumsPictures
        fields = ['id', 'image']


class StadiumsDetailForUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stadiums
        fields = ['id', 'name', 'per_address', 'contact_phone_number', 'price', 'latitude', 'longitude']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["stadium_owner"] = UserSerializers(instance.owner).data
        rep["pictures"] = StadiumsPicturesSerializers(instance.get_all_stadium_pictures(), many=True).data
        return rep


class StadiumsUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stadiums
        fields = ['id', 'name', 'per_address', 'contact_phone_number', 'price', 'latitude', 'longitude']


class StadiumsBookedSerializers(serializers.ModelSerializer):
    class Meta:
        model = StadiumsBooked
        fields = ["id", "starts_time", "ends_time"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["is_busy_now"] = instance.is_busy_now
        rep["booked_client"] = UserSerializers(instance.client).data
        return rep


class StadiumsBookedListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stadiums
        fields = ['id', 'name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["stadium_owner"] = UserSerializers(instance.owner).data

        all_booked_objs = instance.get_all_booked_objs()
        rep['booked'] = StadiumsBookedSerializers(all_booked_objs, many=True).data
        return rep
