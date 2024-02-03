from django.db.models import Count, Q
from rest_framework import generics, response, status

from accounts.enums import AccountRoleEnums
from accounts.models import User
from accounts.permissions import StadiumOwnerAndAdminPermission, UserAndAdminPermission
from main.models import Stadiums, StadiumsBooked
from main.seializers import (
    StadiumsListCreateSerializers, StadiumsUpdateSerializers, StadiumsBookedListSerializers,
    StadiumsDetailForUserSerializers, StadiumsBookedSerializers, StadiumsListForUserSerializers
)


class StadiumsListCreateViews(generics.ListCreateAPIView):
    queryset = Stadiums.objects.all()
    serializer_class = StadiumsListCreateSerializers
    permission_classes = [StadiumOwnerAndAdminPermission]

    def create(self, request, *args, **kwargs):
        if self.request.user.user_roles != AccountRoleEnums.STADIUM_OWNER:
            owner_id = self.request.data.get('owner')
            if owner_id is None:
                return response.Response({
                    "success": False,
                    "err_msg": "owner field is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(id=owner_id, user_roles=AccountRoleEnums.STADIUM_OWNER).exists():
                return response.Response({
                    "success": False,
                    "err_msg": "owner does not exist or role is not stadium owner"
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if self.request.user.user_roles == AccountRoleEnums.STADIUM_OWNER:
            serializer.save(owner=self.request.user)

        else:
            owner_id = self.request.data.get('owner')
            serializer.save(
                owner=User.objects.get(id=owner_id, user_roles=AccountRoleEnums.STADIUM_OWNER)
            )


class StadiumsUpdateViews(generics.UpdateAPIView):
    queryset = Stadiums.objects.all()
    serializer_class = StadiumsUpdateSerializers
    permission_classes = [StadiumOwnerAndAdminPermission]
    http_method_names = ["patch"]


class StadiumsBookedListView(generics.ListAPIView):
    queryset = Stadiums.objects.all()
    serializer_class = StadiumsBookedListSerializers
    permission_classes = [StadiumOwnerAndAdminPermission]


class StadiumsBookedDeleteView(generics.GenericAPIView):
    permission_classes = [StadiumOwnerAndAdminPermission]

    def delete(self, request, booked_id):
        booked = StadiumsBooked.objects.get(pk=booked_id)

        if request.user.user_roles == AccountRoleEnums.STADIUM_OWNER:
            if booked.stadium.owner != request.user:
                return response.Response({
                    "success": False,
                    "err_msg": "you are not owner of the book's stadium"
                }, status=status.HTTP_400_BAD_REQUEST)

        booked.delete()
        return response.Response({
            "success": True,
            "err_msg": ""
        }, status=status.HTTP_200_OK)


# api For users
class StadiumsDetailViews(generics.RetrieveAPIView):
    queryset = Stadiums.objects.all()
    serializer_class = StadiumsDetailForUserSerializers
    permission_classes = [UserAndAdminPermission]


class StadiumsBookedCreateViews(generics.GenericAPIView):
    serializer_class = StadiumsBookedSerializers
    permission_classes = [UserAndAdminPermission]

    def post(self, request, stadium_id):
        if self.request.user.user_roles != AccountRoleEnums.USER:
            client_id = self.request.data.get('client')
            if client_id is None:
                return response.Response({
                    "success": False,
                    "err_msg": "client field is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            if not User.objects.filter(id=client_id, user_roles=AccountRoleEnums.USER).exists():
                return response.Response({
                    "success": False,
                    "err_msg": "client does not exist or role is not user"
                }, status=status.HTTP_400_BAD_REQUEST)

        stadium = Stadiums.objects.get(id=stadium_id)
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)

        if self.request.user.user_roles == AccountRoleEnums.USER:
            serializers.save(
                stadium=stadium,
                client=request.user
            )

        else:
            client_id = self.request.data.get('client')
            serializers.save(
                stadium=stadium,
                client=User.objects.get(id=client_id, user_roles=AccountRoleEnums.USER)
            )

        return response.Response({
            "success": True,
            **serializers.data
        }, status=status.HTTP_201_CREATED)


class StadiumsListForUserViews(generics.GenericAPIView):
    serializer_class = StadiumsListForUserSerializers
    permission_classes = [UserAndAdminPermission]

    def post(self, request, *args, **kwargs):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        starts_time = request.data.get("starts_time")
        ends_time = request.data.get("ends_time")

        if starts_time and ends_time:
            # Filter Stadiums without bookings for the specified time range
            stadiums = Stadiums.objects.annotate(
                num_bookings=Count('stadiums_booked', filter=Q(
                    stadiums_booked__ends_time__gt=starts_time,
                    stadiums_booked__starts_time__lt=ends_time
                ))
            ).filter(num_bookings=0)

        else:
            return response.Response(status=status.HTTP_204_NO_CONTENT)

        if latitude and longitude:
            # Retrieve the queryset of stadiums sorted by closest distance
            stadiums = Stadiums.closest_to_location(latitude, longitude)

        return response.Response({
            "success": True,
            "data": self.serializer_class(stadiums, many=True).data
        })
