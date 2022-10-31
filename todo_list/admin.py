from django.contrib import admin

import todo_list.models.consumption
import todo_list.models.tasks
import todo_list.models.training
# Register your models here.
from todo_list import models


class WorkoutActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)


class DailyTrainingAdmin(admin.ModelAdmin):
    list_display = ('activity', 'date', 'the_series', 'done')
    list_filter = ('date', 'user')


class LongTermTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'done', 'user')
    list_filter = ('user', 'done')


class ConsumptionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    sortable_by = ('name',)


class DailyConsumptionAdmin(admin.ModelAdmin):
    list_display = ('category', 'volume', 'date', 'user')
    list_filter = ('date', 'user')
    sortable_by = ('date',)


admin.site.register(todo_list.models.training.WorkoutActivity, WorkoutActivityAdmin)
admin.site.register(todo_list.models.training.DailyTraining, DailyTrainingAdmin)
admin.site.register(todo_list.models.tasks.LongTermTask, LongTermTaskAdmin)
admin.site.register(todo_list.models.consumption.ConsumptionCategory, ConsumptionCategoryAdmin)
admin.site.register(todo_list.models.consumption.DailyConsumption, DailyConsumptionAdmin)
