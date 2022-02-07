from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import QuestionAnswer
from api.serializers.answer_serializers import AnswerSerializer


class ListCreateQuestionAnswerView(ListCreateAPIView):

    serializer_class = AnswerSerializer
    filterset_fields = ["answer"]

    def get_queryset(self):
        if self.request.user.is_admin:
            return QuestionAnswer.objects.all()
        return QuestionAnswer.objects.filter(question__quiz__user=self.request.user)


class RetrieveUpdateDestroyQuestionAnswerView(RetrieveUpdateDestroyAPIView):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return QuestionAnswer.objects.all()
        return QuestionAnswer.objects.filter(question__quiz__user=self.request.user)
