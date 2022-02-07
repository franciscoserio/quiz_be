from rest_framework.generics import RetrieveAPIView
from api.models import Quiz
from api.serializers.quiz_serializers import QuizStatusSerializer


class StatusQuizView(RetrieveAPIView):

    serializer_class = QuizStatusSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(id=self.kwargs.get("pk"), user=self.request.user)
