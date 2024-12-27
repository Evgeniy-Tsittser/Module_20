from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from django.http import HttpResponse

from .models import MonthWorks, WaterTable, SeverageTable
from decimal import Decimal

"""Функция создания объектов и изменения значений в годовых таблицах:
 - после записи выполненных работ за месяц в таблице MonthWorks при сохранении отправляется сигнал,
 - данная функция при получении этого сигнала создает объекты в таблицах WaterTable, SeverageTable
 в зависимости от выбранного вида работ (1 или 2),
 -  изменяет значения в таблицах WaterTable, SeverageTable, если такие изменения были произведены 
 в таблице MonthWorks"""


@receiver(post_save, sender=MonthWorks)
def update_aggregate_tables(sender, instance, created, **kwargs):
    """связывание названия месяца с его номером"""
    month_field = {1: "january", 2: "february", 3: "march", 4: "april",
                   5: "may", 6: "june", 7: "july", 8: "august",
                   9: "september", 10: "october", 11: "november", 12: "december"}

    if created:
        """если объект создается:"""
        if instance.type_work == 1:  # Вода
            water_table, _ = WaterTable.objects.get_or_create(
                completed_works=instance.completed_works,
                year=instance.year
            )
            """динамическое задание значения атрибуту"""
            setattr(water_table, f"{month_field[instance.month]}_vol", instance.volume)
            setattr(water_table, f"{month_field[instance.month]}_summ", instance.summ)

            water_table.save()  # Сохраняем изменения в таблице воды

        elif instance.type_work == 2:  # Канализация
            severage_table, _ = SeverageTable.objects.get_or_create(
                completed_works=instance.completed_works,
                year=instance.year
            )
            setattr(severage_table, f"{month_field[instance.month]}_vol", instance.volume)
            setattr(severage_table, f"{month_field[instance.month]}_summ", instance.summ)

            severage_table.save()  # Сохраняем изменения в таблице канализации
    else:
        """Обработка изменения существующей записи"""
        if instance.type_work == 1:
            water_table = WaterTable.objects.get(completed_works=instance.completed_works, year=instance.year)
            setattr(water_table, f"{month_field[instance.month]}_vol", instance.volume)
            setattr(water_table, f"{month_field[instance.month]}_summ", instance.summ)

            water_table.save()  # Сохраняем изменения в таблице воды

        elif instance.type_work == 2:
            severage_table = SeverageTable.objects.get(completed_works=instance.completed_works, year=instance.year)
            setattr(severage_table, f"{month_field[instance.month]}_vol", instance.volume)
            setattr(severage_table, f"{month_field[instance.month]}_summ", instance.summ)

            severage_table.save()  # Сохраняем изменения в таблице канализации


"""Функция удаления объектов в годовых таблицах:
 - получает значения по полю completed_works за весь требуемый год,
 - проверяет, есть ли в каких-нибудь месяцах значения, отличные от нуля,
 -  если такие значения есть, то обнуляет значения в таблицах WaterTable, SeverageTable 
 только за выбранный месяц,
 - если все значения по полю completed_works за весь требуемый год равны нулю, 
 то полностью удаляет строку с видом работ
  - вызывает исключения, если таблицы не неайдены"""


@receiver(pre_delete, sender=MonthWorks)
def delete_from_aggregate_tables(sender, instance, **kwargs):
    """связывание названия полей соответствующего месяца с его номером"""
    month_fields = {
        1: ('january_vol', 'january_summ'),
        2: ('february_vol', 'february_summ'),
        3: ('march_vol', 'march_summ'),
        4: ('april_vol', 'april_summ'),
        5: ('may_vol', 'may_summ'),
        6: ('june_vol', 'june_summ'),
        7: ('july_vol', 'july_summ'),
        8: ('august_vol', 'august_summ'),
        9: ('september_vol', 'september_summ'),
        10: ('october_vol', 'october_summ'),
        11: ('november_vol', 'november_summ'),
        12: ('december_vol', 'december_summ'),
    }

    if instance.type_work == 1:  # Вода
        try:
            """Получение всех значений по полю completed_works за выбранный год"""
            water_table = WaterTable.objects.get(completed_works=instance.completed_works, year=instance.year)

            is_non_zero = False

            """Проверка значений за другие месяцы"""
            for month, (vol_field, summ_field) in month_fields.items():
                if month != instance.month:  # Проверяем только остальные месяцы
                    if getattr(water_table, vol_field) > 0 or getattr(water_table, summ_field) > 0:
                        is_non_zero = True
                        break

            if is_non_zero:
                """Обнуляем значения за текущий месяц"""
                if instance.month in month_fields:
                    vol_field, summ_field = month_fields[instance.month]
                    setattr(water_table, vol_field, 0.0)  # Обнуляем volume
                    setattr(water_table, summ_field, 0.00)  # Обнуляем summ
                    water_table.save()
            else:
                """Все значения равны 0, поэтому удаляем запись"""
                water_table.delete()

        except WaterTable.DoesNotExist:
            return HttpResponse("Таблица 'Годовая водоснабжение' не найдена.", status=404)

    elif instance.type_work == 2:  # Канализация
        try:
            severage_table = SeverageTable.objects.get(completed_works=instance.completed_works, year=instance.year)
            is_non_zero = False

            """Проверка значений за другие месяцы"""
            for month, (vol_field, summ_field) in month_fields.items():
                if month != instance.month:  # Проверяем только остальные месяцы
                    if getattr(severage_table, vol_field) > 0 or getattr(severage_table, summ_field) > 0:
                        is_non_zero = True
                        break

            if is_non_zero:
                """Обнуляем значения за текущий месяц"""
                if instance.month in month_fields:
                    vol_field, summ_field = month_fields[instance.month]
                    setattr(severage_table, vol_field, 0.0)  # Обнуляем volume
                    setattr(severage_table, summ_field, 0.00)  # Обнуляем summ
                    severage_table.save()
            else:
                """Все значения равны 0, поэтому удаляем запись"""
                severage_table.delete()
        except SeverageTable.DoesNotExist:
            return HttpResponse("Таблица 'Годовая водоотведение' не найдена.", status=404)


"""Функция суммирования значений поля month_summ по кварталам и году 
 в годовых таблицах WaterTable, SeverageTable:
 - как только в поле month_summ появится значение, функция автоматически прибавит 
 это значение к значению соответствующего квартала и года"""


@receiver(pre_save, sender=WaterTable)
@receiver(pre_save, sender=SeverageTable)
def calculate_totals(sender, instance, **kwargs):
    """Рассчет первого квартала"""
    instance.first_quarter = (
            Decimal(instance.january_summ or 0) +
            Decimal(instance.february_summ or 0) +
            Decimal(instance.march_summ or 0)
    )

    """Рассчет второго квартала"""
    instance.second_quarter = (
            Decimal(instance.april_summ or 0)
            + Decimal(instance.may_summ or 0)
            + Decimal(instance.june_summ or 0)
    )

    """Рассчет третьего квартала"""
    instance.third_quarter = (
            Decimal(instance.july_summ or 0)
            + Decimal(instance.august_summ or 0)
            + Decimal(instance.september_summ or 0)
    )

    """Рассчет четвертого квартала"""
    instance.fourth_quarter = (
            Decimal(instance.october_summ or 0)
            + Decimal(instance.november_summ or 0)
            + Decimal(instance.december_summ or 0)
    )

    """Рассчет общего итога за год"""
    instance.year_total = (
            instance.first_quarter +
            instance.second_quarter +
            instance.third_quarter +
            instance.fourth_quarter
    )