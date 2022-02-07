from datetime import datetime
from uuid import UUID
from api.models import Account, Participant, ParticipantAnswer, Question


def calculate_time_left(datetime_limit: str):
    if datetime_limit is None:
        return None

    now = datetime.now()
    datetime_limit_obj = datetime.strptime(
        datetime_limit.split(".")[0], "%Y-%m-%dT%H:%M:%S"
    )
    now = datetime_limit_obj - now
    if now.total_seconds() < 0:
        return 0
    return int(now.total_seconds())


def total_questions_answered(quiz_id: UUID):
    questions_quantity = Question.objects.filter(quiz_id=quiz_id).count()
    participants_quantity = Participant.objects.filter(quiz_id=quiz_id).count()

    total_expected_answers = participants_quantity * questions_quantity
    participant_answers_quantity = ParticipantAnswer.objects.filter(
        quiz_id=quiz_id, answered_at__isnull=False
    ).count()

    return (participant_answers_quantity / total_expected_answers) * 100


def questions_answered(quiz_id: UUID, user: Account):
    participant_answers_quantity = ParticipantAnswer.objects.filter(
        quiz_id=quiz_id, user=user, answered_at__isnull=False
    ).count()
    return participant_answers_quantity


def questions_left(quiz_id: UUID, user: Account):
    questions_quantity = Question.objects.filter(quiz_id=quiz_id).count()
    participant_answers_quantity = ParticipantAnswer.objects.filter(
        quiz_id=quiz_id, user=user, answered_at__isnull=False
    ).count()
    return questions_quantity - participant_answers_quantity
