from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError("User must have a email address")

        if not first_name:
            raise ValueError("User must have a first name")

        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=200, unique=True)
    date_joined = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=True)
    token_confirmation = models.CharField(max_length=100, unique=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="first_name", max_length=30)
    last_name = models.CharField(verbose_name="last_name", max_length=30)
    is_active = models.BooleanField(default=True)
    quiz = models.ManyToManyField(
        "account", related_name="quizzes", through="Participant"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def create(self, validated_data):
        return Account.objects.create(**validated_data)


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="creator")
    name = models.CharField(max_length=50, unique=False)
    description = models.CharField(max_length=500, unique=False)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)
    question_time_limit = models.IntegerField(null=True, default=None)
    datetime_limit = models.DateTimeField(null=True, default=None)

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def create(self, validated_data):
        return Participant.objects.create(**validated_data)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=200, unique=False)
    created_at = models.DateTimeField(verbose_name="created_at", auto_now_add=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class QuestionAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.CharField(max_length=200, unique=False)
    is_correct = models.BooleanField(default=True)

    def create(self, validated_data):
        return QuestionAnswer.objects.create(**validated_data)


class ParticipantAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, null=True)
    started_at = models.DateTimeField(
        verbose_name="started_at", auto_now=False, null=True
    )
    answered_at = models.DateTimeField(
        verbose_name="answered_at", auto_now=False, null=True
    )

    def create(self, validated_data):
        return ParticipantAnswer.objects.create(**validated_data)
