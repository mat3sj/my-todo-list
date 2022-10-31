import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateWorkoutPlan(forms.Form):
    the_series = forms.CharField(label='Series', max_length=200)
    date = forms.DateField(label='Date',
                           initial=datetime.date.today() + datetime.timedelta(
                               days=1))
    # todo add activity


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']