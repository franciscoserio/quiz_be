from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from api.models import Participant
from api.serializers.participant_serializers import ParticipantSerializer


class ListCreateParticipantView(ListCreateAPIView):

    serializer_class = ParticipantSerializer
    filterset_fields = ["id", "user__email", "user__first_name", "user__last_name"]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Participant.objects.all()
        return Participant.objects.filter(quiz__user=self.request.user)


class DestroyParticipantView(DestroyAPIView):

    serializer_class = ParticipantSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Participant.objects.all()
        return Participant.objects.filter(quiz__user=self.request.user)
