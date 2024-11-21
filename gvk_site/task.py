from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Subscribers
from smsaero import SmsAero, SmsAeroException

SMSAERO_EMAIL = 'evgenc1980@mail.ru'
SMSAERO_API_KEY = 'tJuLoVucxZaSxxO8xKmAfoilFD6'

#Функция отправки СМС-сообщения
def send_sms(phone: int, message: str) -> dict:
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    return api.send_sms(phone, message)

#Функция проверки даты поверки водосчетчика (для Celery)
@shared_task
def send_verification_reminders():
    today = timezone.now().date()
    threshold_date = today + timedelta(days=60)  # 60 дней вперед

    subscribers = Subscribers.objects.filter(verifi_period=threshold_date)

    for subscriber in subscribers:
        message = f"Поверка вашего водосчетчика заканчивается {subscriber.verifi_period}."
        try:
            send_sms(subscriber.telephone_number, message)  # Отправка SMS
        except SmsAeroException as e:
            print(f"Произошла ошибка:  {e}, SMS не отправлено.")
