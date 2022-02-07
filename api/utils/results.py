from datetime import datetime
from uuid import UUID
from api.models import Account, Participant, ParticipantAnswer, Question, Quiz
from api.utils.background_tasks import send_results_email


def participants_results(quiz_id: UUID):

    results = list()

    questions_quantity = Question.objects.filter(quiz_id=quiz_id).count()
    participants = Participant.objects.filter(quiz_id=quiz_id)

    for participant in participants:
        participant_response_data = dict()
        participant_response_data["id"] = participant.user.id
        participant_response_data["email"] = participant.user.email
        participant_response_data["first_name"] = participant.user.first_name
        participant_response_data["last_name"] = participant.user.last_name

        correct_answers = 0
        participant_answers = ParticipantAnswer.objects.filter(
            quiz_id=quiz_id, user=participant.user, answered_at__isnull=False
        )
        for participant_answer in participant_answers:
            if participant_answer.answer.is_correct is True:
                correct_answers = correct_answers + 1

        participant_response_data["result"] = (
            correct_answers / questions_quantity
        ) * 100
        results.append(participant_response_data)

    return results


def send_participants_results(quiz_id: UUID):

    questions_quantity = Question.objects.filter(quiz_id=quiz_id).count()
    participants = Participant.objects.filter(quiz_id=quiz_id)

    for participant in participants:

        correct_answers = 0
        participant_answers = ParticipantAnswer.objects.filter(
            quiz_id=quiz_id, user=participant.user, answered_at__isnull=False
        )
        for participant_answer in participant_answers:
            if participant_answer.answer.is_correct is True:
                correct_answers = correct_answers + 1

        result = (correct_answers / questions_quantity) * 100
        send_results_email.delay(
            participant.user.email,
            participant.quiz.name,
            result,
        )

    return True
