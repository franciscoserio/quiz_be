from api.tests.test_setup import TestSetUp


class TestLogin(TestSetUp):
    def test_correct_login_with_admin(self):
        body = {"email": self.admin_email, "password": self.admin_password}
        res = self.client.post(self.login_url, body, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"]["email"], self.admin_email)
        self.assertEqual(res.data["user"]["first_name"], self.admin_first_name)
        self.assertEqual(res.data["user"]["last_name"], self.admin_last_name)

    def test_correct_login_with_creator(self):
        body = {"email": self.creator_email, "password": self.creator_password}
        res = self.client.post(self.login_url, body, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"]["email"], self.creator_email)
        self.assertEqual(res.data["user"]["first_name"], self.creator_first_name)
        self.assertEqual(res.data["user"]["last_name"], self.creator_last_name)

    def test_correct_login_with_participant(self):
        body = {"email": self.participant_email, "password": self.participant_password}
        res = self.client.post(self.login_url, body, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"]["email"], self.participant_email)
        self.assertEqual(res.data["user"]["first_name"], self.participant_first_name)
        self.assertEqual(res.data["user"]["last_name"], self.participant_last_name)

    def test_incorrect_login(self):
        body = {"email": "incorrect_email@email.com", "password": "incorrect_password"}
        res = self.client.post(self.login_url, body, format="json")
        self.assertEqual(res.status_code, 400)
