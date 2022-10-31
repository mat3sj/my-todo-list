from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
    default_series = models.CharField(max_length=200)

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