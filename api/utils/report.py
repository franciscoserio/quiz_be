from dataclasses import dataclass, field
from django.utils.timezone import datetime
from typing import Optional
from api.models import Quiz
from api.utils.results import participants_results
from dataclass_csv import DataclassWriter


@dataclass
class Report:
    id: str
    name: str
    description: str
    participant_email: Optional[str] = field(default=None)
    participant_first_name: Optional[str] = field(default=None)
    participant_last_name: Optional[str] = field(default=None)
    participant_result: Optional[float] = field(default=None)


def report_to_csv():

    results = get_daily_report()

    final_result = list()

    for quiz_result in results["results"]:
        if len(quiz_result["participants"]) == 0:
            result = Report(
                id=quiz_result["id"],
                name=quiz_result["name"],
                description=quiz_result["description"],
            )
            final_result.append(result)
        else:
            for participant_result in quiz_result["participants"]:
                result = Report(
                    id=quiz_result["id"],
                    name=quiz_result["name"],
                    description=quiz_result["description"],
                    participant_email=participant_result["email"],
                    participant_first_name=participant_result["first_name"],
                    participant_last_name=participant_result["last_name"],
                    participant_result=participant_result["result"],
                )
                final_result.append(result)

    try:
        with open("report.csv", "w") as f:
            w = DataclassWriter(f, final_result, Report)
            w.write()

        return True

    except Exception as e:
        print(e)
        return False


def get_daily_report():

    today = datetime.today()

    response = dict()
    response["results"] = list()

    quiz_obj = Quiz.objects.filter(created_at__day=today.day)
    for quiz in quiz_obj:
        quiz_result = dict()
        quiz_result["id"] = quiz.id
        quiz_result["name"] = quiz.name
        quiz_result["description"] = quiz.description
        participant_results = participants_results(quiz.id)
        quiz_result["participants"] = participant_results
        response["results"].append(quiz_result)

    return response
