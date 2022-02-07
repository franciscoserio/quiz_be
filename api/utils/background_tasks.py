from uuid import UUID, uuid4
from api.utils.send_email import SendEmail
from quiz.celery import app


@app.task(name="send_confirmation_email")
def send_confirmation_email(email: str, token_confirmation: str):
    send_email = SendEmail()
    send_email.user_confirmation(email, token_confirmation)

    if send_email.sent is False:
        print(send_email.error_message)


@app.task(name="send_quiz_invitation_email")
def send_quiz_invitation_email(email: str, quiz_id: UUID, quiz_name: str):
    send_email = SendEmail()
    send_email.quiz_invitation(email, quiz_id, quiz_name)

    if send_email.sent is False:
        print(send_email.error_message)


@app.task(name="send_results_email")
def send_results_email(email: str, quiz_name: str, quiz_result: str):
    send_email = SendEmail()
    send_email.quiz_results(email, quiz_name, quiz_result)

    if send_email.sent is False:
        print(send_email.error_message)
