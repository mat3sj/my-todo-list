import datetime
from typing import Dict

from django.contrib.auth.models import User
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from todo_list import forms
from todo_list import models


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class HomeView(View):
    def get(self, request):
        tasks = _get_todays_tasks(request)
        return render(request, 'home.html', tasks)

    def post(self, request):
        if request.POST.get('newItem'):
            name = request.POST.get('new')
            models.LongTermTask.objects.create(name=name, user=request.user,
                                               value=request.POST.get(
                                                   'new-value', 1))

        elif request.POST.get('save'):
            long_term_tasks = models.LongTermTask.objects.filter(done=False,
                                                                 user=request.user)
            for long_term_task in long_term_tasks:
                if request.POST.get('c' + str(long_term_task.id)) == 'clicked':
                    long_term_task.done = True
                    long_term_task.save()
        tasks = _get_todays_tasks(request)
        return render(request, 'home.html', tasks)


def _get_todays_tasks(request) -> Dict:
    long_term_tasks = models.LongTermTask.objects.filter(done=False,
                                                         user=request.user)
    today_tasks = {}
    try:
        todays_water = models.WaterIncome.objects.get(
            date=datetime.date.today(), user=request.user).volume
    except models.WaterIncome.DoesNotExist:
        todays_water = 0
    tasks = {
        'long_term_tasks': long_term_tasks,
        'today_tasks': today_tasks,
        'todays_water': todays_water}
    return tasks


class DailyWorkoutListView(View):
    def get(self, request):
        workouts = models.DailyTraining.objects.filter(user=1)  # todo change
        response = """workouts:
        """
        for workout in workouts:
            response += f"""{workout.activity.name}
            """
        return HttpResponse(response)


class PlanWorkoutView(View):
    def get(self, request):
        form = forms.CreateWorkoutPlan()
        return render(request, 'workout/create_plan.html', {'form': form})

    def post(self, request):
        form = forms.CreateWorkoutPlan(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            training = models.DailyTraining.objects.create(
                user=request.user,  # todo change
                activity=models.WorkoutActivity.objects.get(pk=1),
                # todo change
                the_series=cleaned_data['the_series'],
                date=cleaned_data['date'],
                done=False
            )
        return HttpResponseRedirect("/")


class WaterIncomeView(View):
    def get(self, request):
        form = forms.WaterIncomeForm()
        return render(request, 'water/water.html', {'form': form})

    def post(self, request):
        form = forms.WaterIncomeForm(request.POST)

        if form.is_valid():
            try:
                todays_water_income = models.WaterIncome.objects.get(
                    date=datetime.date.today())
            except models.WaterIncome.DoesNotExist:
                todays_water_income = models.WaterIncome.objects.create(
                    date=datetime.date.today(),
                    user=request.user,
                    volume=0)
            cleaned_data = form.cleaned_data
            todays_water_income.volume += (cleaned_data['half_a_liter'] * 0.5 +
                                           cleaned_data['three_dl'] * 0.3)
            todays_water_income.save()

        return HttpResponseRedirect("/")
