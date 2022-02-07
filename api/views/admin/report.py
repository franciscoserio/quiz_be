from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from api.models import Quiz
from api.permissions import IsAdmin
from api.serializers.admin.report_serializers import ReportSerializer
from django.utils.timezone import datetime
from api.utils.report import report_to_csv
from django.http import HttpResponse
from rest_framework import serializers
import csv


class ReportView(ListAPIView):

    permission_classes = [IsAdmin]
    serializer_class = ReportSerializer

    def get_queryset(self):
        today = datetime.today()
        return Quiz.objects.filter(created_at__day=today.day)


class ReportCSVView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request, format=None):

        if not report_to_csv():
            raise serializers.ValidationError(
                {"error": ["an error occurred, please try again"]}
            )

        http_resp = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="report.csv"'},
        )

        writer = csv.writer(http_resp)

        with open("report.csv", newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                writer.writerow(row)

        return http_resp
