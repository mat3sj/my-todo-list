import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from todo_list.models.consumption import ConsumptionCategory, DailyConsumption


class DayConsumptionView(View):
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
        categories = ConsumptionCategory.objects.filter(
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


def _get_consumption_categories(user, date=datetime.date.today()) -> dict:
    consumption_dict = {}

    categories = ConsumptionCategory.objects.filter(
        user=user)
    for category in categories:
        try:
            daily = DailyConsumption.objects.get(
                date=date, user=user,
                category=category)
        except DailyConsumption.DoesNotExist:
            daily = DailyConsumption.objects.create(
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


def _get_daily_consumption(user: User, category: ConsumptionCategory,
                           date=datetime.date.today()) -> DailyConsumption:
    try:
        return DailyConsumption.objects.get(
            date=date, user=user,
            category=category)
    except DailyConsumption.DoesNotExist:
        return DailyConsumption.objects.create(
            user=user, category=category, date=date)
