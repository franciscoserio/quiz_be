from uuid import UUID
from django.core.mail import send_mail
from django.conf import settings


class SendEmail:
    def __init__(self):
        self.sent = False
        self.error_message = None

    def user_confirmation(self, email: str, token_confirmation: str):

        subject = "[QUIZ] - User confirmation"
        message = (
            "Please confirm your email on the next link: "
            + settings.HOST_API
            + "api/users/confirmation?token_confirmation="
            + token_confirmation
        )
        try:
            result = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            if result == 1:
                self.sent = True

        except Exception as e:
            self.error_message = e

    def quiz_invitation(self, email: str, quiz_id: UUID, quiz_name: str):
        subject = "[QUIZ] - Invitation for the quiz " + quiz_name
        message = (
            "You can complete the quiz on the next link: "
            + settings.HOST_API
            + "api/participant/quizzes/"
            + str(quiz_id)
        )
        try:
            result = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            if result == 1:
                self.sent = True

        except Exception as e:
            self.error_message = e

    def quiz_results(self, email: str, quiz_name: str, quiz_result: float):
        subject = "[QUIZ] - Results of the quiz " + quiz_name
        message = "Your result was: " + str(quiz_result)
        try:
            result = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            if result == 1:
                self.sent = True

        except Exception as e:
            self.error_message = e
