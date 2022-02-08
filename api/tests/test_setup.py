from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Account


class TestSetUp(APITestCase):
    def setUp(self):
        self.login_url = reverse("login")

        self.admin_first_name = "Admin"
        self.admin_last_name = "Admin"
        self.admin_email = "admin1@email.com"
        self.admin_password = "password"

        self.creator_first_name = "Creator"
        self.creator_last_name = "One"
        self.creator_email = "creator1@email.com"
        self.creator_password = "password"

        self.participant_first_name = "Participant"
        self.participant_last_name = "One"
        self.participant_email = "participant1@email.com"
        self.participant_password = "password"

        # add admin user
        Account.objects.create_superuser(
            first_name=self.admin_first_name,
            last_name=self.admin_last_name,
            email=self.admin_email,
            password=self.admin_password,
        )

        # add creator user
        Account.objects.create(
            first_name=self.creator_first_name,
            last_name=self.creator_last_name,
            email=self.creator_email,
            password=make_password(self.creator_password),
            is_admin=False,
        )

        # add creator participant
        Account.objects.create(
            first_name=self.participant_first_name,
            last_name=self.participant_last_name,
            email=self.participant_email,
            password=make_password(self.participant_password),
            is_admin=False,
        )

        # get creator user token
        body = {"email": self.creator_email, "password": self.creator_password}
        res = self.client.post(self.login_url, body, format="json")
        self.creator_token = res.data["token"]

        return super().setUp()
