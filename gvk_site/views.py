import logging
from .models import Tariffs, Quality
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Subscribers
from .forms import LoginForm
from django.shortcuts import render, get_object_or_404

logger = logging.getLogger(__name__)


# Представление Главной страницы
def home_views(request):
    logger.info("Доступ к главной странице сайта.")
    return render(request, 'gvk_site/home_page.html')


# Представление страницы О предприятии
def about_views(request):
    logger.info("Доступ к странице О предприятии.")
    return render(request, 'gvk_site/about_page.html')


# Представление страницы Тарифы
def tariffs_views(request):
    logger.info("Доступ к странице с тарифами.")
    tariffs = Tariffs.objects.all()
    context = {'tariffs': tariffs, }
    return render(request, 'gvk_site/tariffs_page.html', context)


# Представление страницы Качество воды
def quality_views(request):
    logger.info("Доступ к странице качества воды.")
    qualities = Quality.objects.all()
    context = {'qualities': qualities}
    return render(request, 'gvk_site/quality_page.html', context)


# Представление страницы Контакты
def contacts_views(request):
    logger.info("Доступ к странице контактов.")
    return render(request, 'gvk_site/contacts_page.html')


# Представление страницы Авторизация
def login_view(request):
    logger.info("Доступ к странице авторизации.")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.info(f"Форма валидна. Пользователь: {username}")

            try:
                subscriber = Subscribers.objects.get(login=username)
            except Subscribers.DoesNotExist:
                context = {'form': form, 'error_message': 'Неверный логин или пароль'}
                return render(request, 'gvk_site/login.html', context)

            # Проверка пароля
            if check_password(password, subscriber.password):
                request.session['subscriber_id'] = subscriber.id
                # Переход на страницу личного кабинета
                return redirect('personal_cabinet', pk=subscriber.pk)
            else:
                context = {'form': form, 'error_message': 'Неверный логин или пароль'}
                return render(request, 'gvk_site/login.html', context)

        else:
            logger.error("Форма невалидна: %s", form.errors)  # Логируем ошибки формы
    else:
        form = LoginForm()

    return render(request, 'gvk_site/login.html', {'form': form})


# Представление страницы Личный кабинет
def personal_cabinet_view(request, pk):
    logger.info("Доступ к странице личного кабинета.")
    subscriber = get_object_or_404(Subscribers, pk=pk)
    context = {
        'subscriber': subscriber,
        'greeting': f'Приветствую, {subscriber.name}',
        'address': subscriber.address,
        'metering_device_number': subscriber.metering_device_number,
        'damage_data': subscriber.damage_data,
        'verifi_period': subscriber.verifi_period,
    }
    return render(request, 'gvk_site/personal_cabinet.html', context)
