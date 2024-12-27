from django.contrib import admin
from .models import Subscribers, Address, Tariffs, Quality, MonthWorks, WaterTable, SeverageTable, Employee


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ("address", "name", "verifi_period",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address",)


@admin.register(Tariffs)
class TariffsAdmin(admin.ModelAdmin):
    list_display = ("water_ch", "water_push", "sewerage",)


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ("month",)

@admin.register(MonthWorks)
class MonthWorksAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'completed_works', 'description', 'volume', 'summ')
    list_filter = ('type_work', 'year', 'month')
    search_fields = ['completed_works']


@admin.register(WaterTable)
class WaterTableAdmin(admin.ModelAdmin):
    list_display = ('year', 'completed_works', 'year_total')
    search_fields = ['completed_works']


@admin.register(SeverageTable)
class SeverageTableAdmin(admin.ModelAdmin):
    list_display = ('year', 'completed_works', 'year_total')
    search_fields = ['completed_works']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name",)
