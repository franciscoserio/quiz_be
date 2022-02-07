from datetime import datetime
from uuid import UUID
from api.models import Account, ParticipantAnswer, Question, Quiz


def update_participant_start_date(quiz_id: UUID, question_id: UUID, user: Account):
    question = Question.objects.filter(id=question_id, quiz__participants__user=user)
    if not question:
        return False

    quiz = Quiz.objects.filter(id=quiz_id)
    if not quiz:
        return False

    participant_answer = ParticipantAnswer.objects.filter(
        quiz_id=quiz_id, question_id=question_id, user=user
    )
    if not participant_answer:
        started_at = datetime.now()
        start_participant_answer = ParticipantAnswer(
            quiz_id=quiz_id, question_id=question_id, started_at=started_at, user=user
        )
        start_participant_answer.save()

    return True
