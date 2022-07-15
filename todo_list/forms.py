import datetime

from django import forms


class CreateWorkoutPlan(forms.Form):
    the_series = forms.CharField(label='Series', max_length=200)
    date = forms.DateField(label='Date',
                           initial=datetime.date.today() + datetime.timedelta(
                               days=1))
    # todo add activity


class WaterIncomeForm(forms.Form):
    half_a_liter = forms.IntegerField(label='0.5 l', initial=0)
    three_dl = forms.IntegerField(label='0.3 l', initial=0)
