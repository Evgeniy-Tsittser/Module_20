from django.contrib import admin
from .models import Subscribers, Address, Tariffs, Quality


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


