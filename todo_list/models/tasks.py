from django.contrib.auth.models import User
from django.db import models


class LongTermTask(models.Model):
    """
    Model for keeping long term tasks
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    value = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TodoList(models.Model):
    """
    Classical to do list
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    done = models.BooleanField(default=False)


class TodoListTask(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    details = models.TextField()
    done = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
