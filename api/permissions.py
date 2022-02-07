from rest_framework.permissions import BasePermission
from api.models import Participant, Quiz


class IsAdmin(BasePermission):

    message = {"errors": ["Only admin users have access to this endpoint"]}

    def has_permission(self, request, view):

        # user permissions
        if request.user.is_admin:
            return True

        return False


class IsParticipant(BasePermission):

    message = {"errors": []}

    def has_permission(self, request, view):

        self.message["errors"].clear()

        route = request.resolver_match.route

        try:
            pk = route.split("quizzes/<uuid:")[1].split(">")[0]
        except:
            return True

        quiz = Quiz.objects.filter(id=request.resolver_match.kwargs.get(pk))
        if not quiz:
            self.message["errors"].append("quiz not found")
            return False

        participant_quiz = Participant.objects.filter(
            quiz_id=request.resolver_match.kwargs.get(pk), user=request.user
        )
        if not participant_quiz:
            self.message["errors"].append(
                "Only participant users have access to this endpoint"
            )
            return False

        return True
