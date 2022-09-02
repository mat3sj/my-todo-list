import datetime
from typing import Dict
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from todo_list import forms
from todo_list import models
from todo_list.forms import RegisterForm
from todo_list.models import TodoList, TodoListTask


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
        return render(request, 'water/water_add.html', {'form': form})

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


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html',
                      {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/register")


class WaterView(View):
    def get(self, request):
        return render(request, 'water/water.html')


class TodayConsumptionView(View):
    def get(self, request, date):
        if date == 'today':
            date = datetime.date.today()
        consumption_dict = _get_consumption_categories(user=request.user,
                                                       date=date)
        return render(request, 'consumption/today_consumption.html',
                      {'categories': consumption_dict})

    def post(self, request, date):
        if date == 'today':
            date = datetime.date.today()
        categories = models.ConsumptionCategory.objects.filter(
            user=request.user)
        for category in categories:
            daily = _get_daily_consumption(user=request.user, category=category,
                                           date=date)
            volumes = category.volumes.split(',')
            for volume in volumes:
                form_field_name = f'{category.name}-{volume}'
                if request.POST.get(form_field_name):
                    number = request.POST.get(form_field_name)
                    daily.volume += float(volume) * int(
                        request.POST.get(form_field_name))
            daily.save()

        consumption_dict = _get_consumption_categories(user=request.user)
        return render(request, 'consumption/today_consumption.html',
                      {'categories': consumption_dict})


class TodoListListView(View):

    def get(self, request):
        todo_lists = TodoList.objects.filter(user=request.user)

        return render(request, 'todo_list/todo_list_list.html',
                      {'todo_lists': todo_lists})

    def post(self, request):
        if request.POST.get('newTodoList'):
            name = request.POST.get('new')
            models.TodoList.objects.create(name=name, user=request.user)
        todo_lists = TodoList.objects.filter(user=request.user)

        return render(request, 'todo_list/todo_list_list.html',
                      {'todo_lists': todo_lists})


class TodoListDetailView(View):
    def get(self, request, todo_list_id):
        if TodoList.objects.filter(pk=todo_list_id, user=request.user).exists():
            tasks = TodoListTask.objects.filter(
                todo_list=todo_list_id).order_by('done', 'updated_at')
            return render(
                request, 'todo_list/todo_list_detail.html',
                {
                    'tasks': tasks,
                    'todo_list': models.TodoList.objects.get(pk=todo_list_id)
                })

    def post(self, request, todo_list_id):
        if request.POST.get('newTask'):
            name = request.POST.get('new')
            models.TodoListTask.objects.create(
                task_name=name,
                todo_list=models.TodoList.objects.get(pk=todo_list_id))
        tasks = TodoListTask.objects.filter(
            todo_list=todo_list_id).order_by('done', 'updated_at')
        for task in tasks:
            if request.POST.get('task-' + str(task.id)) == 'clicked':
                task.done = True
                task.save()
        return render(
            request, 'todo_list/todo_list_detail.html',
            {
                'tasks': tasks,
                'todo_list': models.TodoList.objects.get(pk=todo_list_id)
            })


def _get_consumption_categories(user, date=datetime.date.today()) -> dict:
    consumption_dict = {}

    categories = models.ConsumptionCategory.objects.filter(
        user=user)
    for category in categories:
        try:
            daily = models.DailyConsumption.objects.get(
                date=date, user=user,
                category=category)
        except models.DailyConsumption.DoesNotExist:
            daily = models.DailyConsumption.objects.create(
                user=user, category=category)
        volumes = category.volumes.split(',')
        today_volume = int(daily.volume) if isinstance(daily.volume,
                                                       int) or daily.volume.is_integer() else daily.volume
        consumption_dict[category.name] = {
            'name': category.name,
            'volumes': volumes,
            'unit': category.unit,
            'today': today_volume
        }

    return consumption_dict


def _get_daily_consumption(user: User, category: models.ConsumptionCategory,
                           date=datetime.date.today()) -> models.DailyConsumption:
    try:
        return models.DailyConsumption.objects.get(
            date=date, user=user,
            category=category)
    except models.DailyConsumption.DoesNotExist:
        return models.DailyConsumption.objects.create(
            user=user, category=category, date=date)
