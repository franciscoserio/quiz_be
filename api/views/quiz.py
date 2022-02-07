from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import Quiz
from api.serializers.quiz_serializers import QuizSerializer


class ListCreateQuizView(ListCreateAPIView):

    serializer_class = QuizSerializer
    filterset_fields = ["name", "id"]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(user=self.request.user)


class RetrieveUpdateDestroyQuizView(RetrieveUpdateDestroyAPIView):

    serializer_class = QuizSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(user=self.request.user)
