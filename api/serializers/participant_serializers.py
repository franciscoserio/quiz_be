from rest_framework import serializers
from api.models import Account, Participant
from api.serializers.quiz_serializers import QuizSerializer
from api.serializers.user_serializers import UserConfirmationSerializer
from api.utils.background_tasks import (
    send_confirmation_email,
    send_quiz_invitation_email,
)
from django.utils.crypto import get_random_string


class ParticipantSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    user = UserConfirmationSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "email", "first_name", "last_name", "user"]

    def validate(self, data):

        user = Account.objects.filter(email=data["email"])
        if not user:
            if "first_name" not in data or "last_name" not in data:
                raise serializers.ValidationError(
                    {
                        "participant": "user does not exists, please provide the first_name and last_name"
                    }
                )

        user_participant = Participant.objects.filter(user__email=data["email"])
        if user_participant:
            raise serializers.ValidationError(
                {"participant": "user already invited to this quiz"}
            )

        return data

    def create(self, validated_data):

        user = Account.objects.filter(email=validated_data["email"])
        if user:
            participant_data = dict()
            participant_data["quiz_id"] = self.context["view"].kwargs.get("quiz_id")
            participant_data["user_id"] = user[0].id
            participant = Participant.objects.create(**participant_data)

            # send quiz invitation email
            send_quiz_invitation_email.delay(
                validated_data["email"],
                self.context["view"].kwargs.get("quiz_id"),
                participant.quiz.name,
            )
            return participant

        else:
            # create new user
            user_data = dict()
            user_data["token_confirmation"] = get_random_string(length=100)
            user_data["email"] = validated_data["email"]
            user_data["first_name"] = validated_data["first_name"]
            user_data["last_name"] = validated_data["last_name"]
            user_data["is_admin"] = False
            new_user = Account.objects.create(**user_data)

            participant_data = dict()
            participant_data["quiz_id"] = self.context["view"].kwargs.get("quiz_id")
            participant_data["user_id"] = new_user.id
            participant = Participant.objects.create(**participant_data)

            # send confirmation email
            send_confirmation_email.delay(
                validated_data["email"], user_data["token_confirmation"]
            )

            # send quiz invitation email
            send_quiz_invitation_email.delay(
                validated_data["email"],
                self.context["view"].kwargs.get("quiz_id"),
                participant.quiz.name,
            )

            return participant
