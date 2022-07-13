from django.contrib import admin

# Register your models here.
from todo_list import models


class WorkoutActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)


class DailyTrainingAdmin(admin.ModelAdmin):
    list_display = ('activity', 'date', 'the_series', 'done')
    list_filter = ('date', 'user')


class WaterIncomeAdmin(admin.ModelAdmin):
    list_display = ('volume', 'date', 'user')
    list_filter = ('date', 'user')
    sortable_by = ('date', )


admin.site.register(models.WorkoutActivity, WorkoutActivityAdmin)
admin.site.register(models.DailyTraining, DailyTrainingAdmin)
admin.site.register(models.WaterIncome, WaterIncomeAdmin)
