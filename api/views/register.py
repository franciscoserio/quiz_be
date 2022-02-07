from rest_framework.generics import CreateAPIView, UpdateAPIView
from api.models import Account
from api.serializers.user_serializers import (
    RegisterSerializer,
    UserConfirmationSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import serializers


class RegisterView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = Account.objects.all()


class UserConfirmationView(UpdateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserConfirmationSerializer

    def get_object(self):

        if not self.request.GET.get("token_confirmation"):
            raise serializers.ValidationError(
                {"errors": ["token_confirmation parameter is required"]}
            )

        user_object = Account.objects.filter(
            token_confirmation=self.request.GET.get("token_confirmation")
        )

        if not user_object:
            raise serializers.ValidationError({"errors": ["user not found"]})

        if user_object.first().email_confirmed:
            raise serializers.ValidationError({"errors": ["email already confirmed"]})

        return user_object.first()

    def get_queryset(self):

        Account.objects.get(
            token_confirmation=self.request.GET.get("token_confirmation")
        )
