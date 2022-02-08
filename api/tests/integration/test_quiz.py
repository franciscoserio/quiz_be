from api.tests.test_setup import TestSetUp
from django.urls import reverse


class TestQuiz(TestSetUp):
    def test_create_quiz_successfully(self):
        quiz_url = reverse("quizzes")
        body_quiz = {"name": "quiz name", "description": "quiz_description"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.creator_token)
        res_quiz = self.client.post(quiz_url, body_quiz, format="json")
        self.assertEqual(res_quiz.status_code, 201)

    def test_create_quiz_without_name(self):
        quiz_url = reverse("quizzes")
        body_quiz = {"description": "quiz_description"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.creator_token)
        res_quiz = self.client.post(quiz_url, body_quiz, format="json")
        self.assertEqual(res_quiz.status_code, 400)

    def test_create_quiz_with_invalid_question_time_limit(self):
        quiz_url = reverse("quizzes")
        body_quiz = {
            "name": "quiz name 2",
            "description": "quiz_description",
            "question_time_limit": "invalid",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.creator_token)
        res_quiz = self.client.post(quiz_url, body_quiz, format="json")
        self.assertEqual(res_quiz.status_code, 400)
