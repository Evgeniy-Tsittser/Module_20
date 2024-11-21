from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.hashers import make_password


# Модель базы данных адресов
class Address(models.Model):
    address = models.CharField(max_length=200, null=False, unique=True)

    def __str__(self):
        return self.address


# Модель базы данных абонентов
class Subscribers(models.Model):
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    metering_device_number = models.CharField(max_length=200)
    damage_data = models.DateField()
    verifi_period = models.DateField()
    telephone_number = models.CharField(max_length=15)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=120)

    # Функция кэширования пароля
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}, {self.address}, {self.telephone_number}'


# Модель базы данных тарифов
class Tariffs(models.Model):
    water_ch = models.DecimalField(max_digits=10, decimal_places=2)
    water_push = models.DecimalField(max_digits=10, decimal_places=2)
    sewerage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Water: {self.water_ch}, {self.water_push}, Sewerage: {self.sewerage}"


# Модель базы данных качества воды
class Quality(models.Model):
    month = models.CharField(max_length=20)
    iron = models.DecimalField(max_digits=10, decimal_places=2)
    manganese = models.DecimalField(max_digits=10, decimal_places=2)
    turbidity = models.DecimalField(max_digits=10, decimal_places=2)
    rigidity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.month, self.iron, self.manganese, self.turbidity, self.rigidity
