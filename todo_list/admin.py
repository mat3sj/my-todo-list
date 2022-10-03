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
    sortable_by = ('date',)


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


admin.site.register(models.WorkoutActivity, WorkoutActivityAdmin)
admin.site.register(models.DailyTraining, DailyTrainingAdmin)
admin.site.register(models.WaterIncome, WaterIncomeAdmin)
admin.site.register(models.LongTermTask, LongTermTaskAdmin)
admin.site.register(models.ConsumptionCategory, ConsumptionCategoryAdmin)
admin.site.register(models.DailyConsumption, DailyConsumptionAdmin)
