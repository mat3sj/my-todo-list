import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from todo_list import forms
from todo_list.models.training import WorkoutActivity, DailyTraining


class DailyWorkoutListView(View):
    def get(self, request, date):
        if date == 'today':
            date = datetime.date.today()
        workout_dict = _get_workouts(user=request.user, date=date)
        return render(request, )


class PlanWorkoutView(View):
    def get(self, request):
        form = forms.CreateWorkoutPlan()
        return render(request, 'training/create_plan.html', {'form': form})

    def post(self, request):
        form = forms.CreateWorkoutPlan(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            training = DailyTraining.objects.create(
                user=request.user,  # todo change
                activity=WorkoutActivity.objects.get(
                    pk=1),
                # todo change
                the_series=cleaned_data['the_series'],
                date=cleaned_data['date'],
                done=False
            )
        return HttpResponseRedirect("/")


def _get_workouts(user: User, date=datetime.date.today()):
    workout_dict = {}
    activities = WorkoutActivity.objects.filter(user=user)
    for activity in activities:
        try:
            daily = DailyTraining.objects.get(
                user=user, date=date, activity=activity)
        except DailyTraining.DoesNotExist:
            daily = DailyTraining.objects.create(
                user=user, activity=activity, date=date,
                the_series=activity.default_series)
        workout_dict[activity.name] = {
            'done': daily.done,
            'series': daily.the_series,
        }
    return workout_dict
