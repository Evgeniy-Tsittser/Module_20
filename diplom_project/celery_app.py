from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

   # Устанавливаем переменную окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom_project.settings')

app = Celery('diplom_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()