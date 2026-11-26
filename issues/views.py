from django.shortcuts import render
from django.http import JsonResponse
from .models import Issue, CriticalIssue, LowPriorityIssue
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from datetime import datetime
import json
from json import JSONDecodeError
from pathlib import Path
from django.core.serializers.json import DjangoJSONEncoder
import traceback


ISSUES_FILE = Path(__file__).resolve().parent / "issues.json"


def get_issues(request, id=None):
    issue_id = request.GET.get('id')
    status_param = request.GET.get('status')

    with open("issues/issues.json", "r") as file:
        issues = json.load(file)


    if id is None:
        return JsonResponse({"issues": issues})
    for issue in issues:
        if issue["id"] == int(id):
            return JsonResponse(issue)
    return JsonResponse({"error": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def post_issues(request):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            return JsonResponse(
                {"error": "The request body must be a JSON object."},
                status=400,
            )

        priority = data.get("priority")
        issue_data = {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "status": data.get("status"),
            "priority": priority,
            "reporter_id": data.get("reporter_id")
        }

        if priority == "critical":
            issue = CriticalIssue(**issue_data)
        elif priority == "low":
            issue = LowPriorityIssue(**issue_data)
        else:
            issue = Issue(**issue_data)

        issue.validate()

        # Load existing entries, or start with an empty list.
        if ISSUES_FILE.exists():
            with ISSUES_FILE.open("r", encoding="utf-8") as file:
                issues = json.load(file)
            if not isinstance(issues, list):
                return JsonResponse(
                    {"error": "issues.json must contain a JSON list."},
                    status=500,
                )
        else:
            issues = []

        # Add the new entry and write the updated list back.
        issue_dict = issue.to_dict()
        issues.append(issue_dict)

        with ISSUES_FILE.open("w", encoding="utf-8") as file:
            json.dump(issues, file, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder,)

        response_data = issue_dict.copy()
        response_data["message"] = issue.describe()
        return JsonResponse(response_data, status=201)

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must contain valid JSON."}, status=400)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except OSError as exc:
        return JsonResponse({"error": f"Could not save issues.json: {exc}"}, status=500)
