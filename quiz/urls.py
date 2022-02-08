from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from api.views.admin.report import ReportCSVView, ReportView
from api.views.participant.participant import (
    ListParticipantQuizView,
    RetrieveParticipantQuizView,
)
from api.views.participant.question import (
    CreateQuestionAnswerParticipantQuizView,
    RetrieveQuestionAnswerParticipantQuizView,
)
from api.views.participant.quiz_status import StatusQuizParticipantView
from api.views.question import ListCreateQuestionView, RetrieveUpdateDestroyQuestionView
from api.views.question_answer import (
    ListCreateQuestionAnswerView,
    RetrieveUpdateDestroyQuestionAnswerView,
)
from api.views.quiz import ListCreateQuizView, RetrieveUpdateDestroyQuizView
from api.views.register import RegisterView, UserConfirmationView
from api.views.question_participant import (
    DestroyParticipantView,
    ListCreateParticipantView,
)
from api.views.results import NotifyResultsQuizView, ResultsQuizView
from api.views.status import StatusQuizView


urlpatterns = [
    path("api/login", obtain_jwt_token, name="login"),
    path("api/register", RegisterView.as_view()),
    path("api/users/confirmation", UserConfirmationView.as_view()),
    # creators and admin
    path("api/quizzes", ListCreateQuizView.as_view(), name="quizzes"),
    path("api/quizzes/<uuid:pk>", RetrieveUpdateDestroyQuizView.as_view()),
    path("api/quizzes/<uuid:quiz_id>/questions", ListCreateQuestionView.as_view()),
    path(
        "api/quizzes/<uuid:quiz_id>/questions/<uuid:pk>",
        RetrieveUpdateDestroyQuestionView.as_view(),
    ),
    path(
        "api/quizzes/<uuid:quiz_id>/questions/<uuid:question_id>/answers",
        ListCreateQuestionAnswerView.as_view(),
    ),
    path(
        "api/quizzes/<uuid:quiz_id>/questions/<uuid:question_id>/answers/<uuid:pk>",
        RetrieveUpdateDestroyQuestionAnswerView.as_view(),
    ),
    path(
        "api/quizzes/<uuid:quiz_id>/participants", ListCreateParticipantView.as_view()
    ),
    path(
        "api/quizzes/<uuid:quiz_id>/participants/<uuid:pk>",
        DestroyParticipantView.as_view(),
    ),
    path("api/quizzes/<uuid:pk>/status", StatusQuizView.as_view()),
    path("api/quizzes/<uuid:pk>/results", ResultsQuizView.as_view()),
    path("api/quizzes/<uuid:pk>/results/notify", NotifyResultsQuizView.as_view()),
    # participants
    path("api/participant/quizzes", ListParticipantQuizView.as_view()),
    path("api/participant/quizzes/<uuid:pk>", RetrieveParticipantQuizView.as_view()),
    path(
        "api/participant/quizzes/<uuid:quiz_id>/questions/<uuid:pk>",
        RetrieveQuestionAnswerParticipantQuizView.as_view(),
    ),
    path(
        "api/participant/quizzes/<uuid:quiz_id>/questions/<uuid:pk>/answers",
        CreateQuestionAnswerParticipantQuizView.as_view(),
    ),
    path(
        "api/participant/quizzes/<uuid:pk>/status", StatusQuizParticipantView.as_view()
    ),
    # admin
    path("api/admin/reports", ReportView.as_view()),
    path("api/admin/reports/csv", ReportCSVView.as_view()),
]
