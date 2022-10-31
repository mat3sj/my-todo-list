from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

import todo_list.models.consumption
import todo_list.models.tasks
import todo_list.models.training
from todo_list.forms import RegisterForm
from todo_list.views.tasks import _get_todays_tasks


class HomeView(View):
    def get(self, request):
        tasks = _get_todays_tasks(request)
        return render(request, 'home.html', tasks)

    def post(self, request):
        if request.POST.get('newItem'):
            name = request.POST.get('new')
            todo_list.models.tasks.LongTermTask.objects.create(
                name=name, user=request.user,
                value=request.POST.get('new-value', 1))

        elif request.POST.get('save'):
            long_term_tasks = todo_list.models.tasks.LongTermTask.objects.filter(
                done=False,
                user=request.user)
            for long_term_task in long_term_tasks:
                if request.POST.get('c' + str(long_term_task.id)) == 'clicked':
                    long_term_task.done = True
                    long_term_task.save()
        tasks = _get_todays_tasks(request)
        return render(request, 'home.html', tasks)


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
