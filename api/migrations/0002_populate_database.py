from django.db import migrations
from api.models import Account, Participant, Question, QuestionAnswer, Quiz
from django.contrib.auth.hashers import make_password


def init_database(apps, schema_editor):
    # users
    admin = Account(
        email="admin@email.com",
        first_name="Admin",
        last_name="Admin",
        is_admin=True,
        password=make_password("password"),
    )
    admin.save()

    creator1 = Account(
        email="creator@email.com",
        first_name="Creator",
        last_name="One",
        is_admin=False,
        password=make_password("password"),
    )
    creator1.save()

    user_participant1 = Account(
        email="participant@email.com",
        first_name="Participant",
        last_name="one",
        is_admin=False,
        password=make_password("password"),
    )
    user_participant1.save()

    # quiz
    quiz1 = Quiz(
        name="quiz one", description="a description related to the quiz", user=creator1
    )
    quiz1.save()

    # question
    question1 = Question(quiz=quiz1, question="question one")
    question1.save()

    # question answers
    question_answer1 = QuestionAnswer(
        question=question1, answer="answer 1", is_correct=True
    )
    question_answer1.save()

    question_answer2 = QuestionAnswer(
        question=question1, answer="answer 1", is_correct=False
    )
    question_answer2.save()

    # participant
    participant1 = Participant(quiz=quiz1, user=user_participant1)
    participant1.save()


class Migration(migrations.Migration):

    dependencies = [("api", "0001_initial")]

    operations = [
        migrations.RunPython(init_database),
    ]
