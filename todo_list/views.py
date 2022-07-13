import datetime

from django.shortcuts import render

from django.http import HttpResponse
from django.views import View

from todo_list.models import DailyTraining


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class DailyWorkoutListView(View):
    def get(self, request):
        workouts = DailyTraining.objects.filter(user=1)
        response = """workouts:
        """
        for workout in workouts:
            response += f"""{workout.activity.name}
            """
        return HttpResponse(response)

