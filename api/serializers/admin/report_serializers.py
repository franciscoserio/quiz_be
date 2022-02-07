import datetime
from rest_framework import serializers
from api.models import Quiz
from api.utils.results import participants_results
import pandas as pd


class ReportSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def to_representation(self, instance):
        data = super(ReportSerializer, self).to_representation(instance)
        response = dict()
        response["id"] = data["id"]
        response["name"] = data["name"]
        response["description"] = data["description"]
        response["participants"] = participants_results(data["id"])
        return response
