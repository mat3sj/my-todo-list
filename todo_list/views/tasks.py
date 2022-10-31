from typing import Dict

from django.shortcuts import render
from django.views import View

import todo_list.models
from todo_list.models.tasks import TodoList, TodoListTask


class TodoListDetailView(View):
    def get(self, request, todo_list_id):
        if TodoList.objects.filter(pk=todo_list_id, user=request.user).exists():
            tasks = TodoListTask.objects.filter(
                todo_list=todo_list_id).order_by('done', 'updated_at')
            return render(
                request, 'todo_list/todo_list_detail.html',
                {
                    'tasks': tasks,
                    'todo_list': todo_list.models.tasks.TodoList.objects.get(pk=todo_list_id)
                })

    def post(self, request, todo_list_id):
        if request.POST.get('newTask'):
            name = request.POST.get('new')
            todo_list.models.tasks.TodoListTask.objects.create(
                task_name=name,
                todo_list=todo_list.models.tasks.TodoList.objects.get(pk=todo_list_id))
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
                'todo_list': todo_list.models.tasks.TodoList.objects.get(pk=todo_list_id)
            })


class TodoListListView(View):

    def get(self, request):
        todo_lists = TodoList.objects.filter(user=request.user)
        todo_lists_list = []

        for todo_list in todo_lists:
            number_of_tasks = todo_list.models.tasks.TodoListTask.objects.filter(
                todo_list=todo_list
            ).count()

            number_of_done_tasks = todo_list.models.tasks.TodoListTask.objects.filter(
                todo_list=todo_list, done=True
            ).count()
            todo_lists_list.append({
                'the_list': todo_list,
                'num_of_tasks': number_of_tasks,
                'num_of_done_tasks': number_of_done_tasks
            })

        return render(request, 'todo_list/todo_list_list.html',
                      {'todo_lists': todo_lists_list})

    def post(self, request):
        if request.POST.get('newTodoList'):
            name = request.POST.get('new')
            todo_list.models.tasks.TodoList.objects.create(name=name, user=request.user)
        return self.get(request)


def _get_todays_tasks(request) -> Dict:
    long_term_tasks = todo_list.models.tasks.LongTermTask.objects.filter(done=False,
                                                                         user=request.user)
    today_tasks = {}
    tasks = {
        'long_term_tasks': long_term_tasks,
        'today_tasks': today_tasks,
        }
    return tasks
