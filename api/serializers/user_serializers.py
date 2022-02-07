from rest_framework import serializers
from api.models import Account
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from api.utils.background_tasks import send_confirmation_email
from api.utils.send_email import SendEmail


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "first_name", "last_name", "is_admin", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Account
        fields = ["id", "email", "first_name", "last_name", "date_joined"]

    def create(self, validated_data):

        # token confirmation
        validated_data["token_confirmation"] = get_random_string(length=100)

        # set admin to false
        validated_data["is_admin"] = False

        user = Account.objects.create(**validated_data)

        # send email
        send_confirmation_email.delay(
            validated_data["email"], validated_data["token_confirmation"]
        )

        return user


class UserConfirmationSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    email = serializers.UUIDField(read_only=True)
    first_name = serializers.UUIDField(read_only=True)
    last_name = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ["id", "email", "first_name", "last_name", "password"]

    def update(self, instance, validated_data):

        # encrypt password
        validated_data["password"] = make_password(validated_data["password"])
        Account.objects.filter(
            token_confirmation=self.context["request"].query_params[
                "token_confirmation"
            ]
        ).update(password=validated_data["password"], email_confirmed=True)

        return instance
