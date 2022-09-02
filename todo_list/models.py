import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class WorkoutActivity(models.Model):
    """
    model to accomodate details about workout activity
    """

    class Category(models.IntegerChoices):
        REPETITIONS = 1, 'Repetitions'
        SECONDS = 2, 'Seconds'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.IntegerField(choices=Category.choices,
                                   default=Category.REPETITIONS)
    series = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Workout Activities'

    def __str__(self):
        return self.name


class DailyTraining(models.Model):
    """
    Model to hold daily workout
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(WorkoutActivity, on_delete=models.CASCADE)
    the_series = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.activity.name} - {self.date}'


class WaterIncome(models.Model):
    """
    Model to hold water income
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    volume = models.FloatField()


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


class ConsumptionCategory(models.Model):
    """
    Model that holds all income options for user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    volumes = models.CharField(max_length=200)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class DailyConsumption(models.Model):
    """
    Model that holds daily income of IncomeCategory
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ConsumptionCategory,
                                 related_name='income_category',
                                 on_delete=models.CASCADE)
    volume = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'category', 'date')
