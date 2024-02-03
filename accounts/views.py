from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.seializers import LoginSerializers


class LoginViews(TokenObtainPairView):
    serializer_class = LoginSerializers
