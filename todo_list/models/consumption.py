from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
