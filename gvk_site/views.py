import logging
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from .models import Tariffs, Quality, Subscribers, Employee, MonthWorks, WaterTable, SeverageTable, YEAR_CHOICES
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import LoginForm, EmployeeLoginForm
from django.contrib.auth import logout
from io import BytesIO
from reportlab.lib.pagesizes import A4
import qrcode

"""
Подключение логирования для представлений.
"""
logger = logging.getLogger(__name__)

"""
Представление Главной страницы:
 - рендерит шаблон главной страницы.
"""


def home_views(request):
    logger.info("Доступ к главной странице сайта.")
    return render(request, 'gvk_site/home_page.html')


"""
Представление страницы О предприятии:
 - рендерит шаблон страницы "О предприятии".
"""


def about_views(request):
    logger.info("Доступ к странице О предприятии.")
    return render(request, 'gvk_site/about_page.html')


"""
Представление страницы Тарифы:
 - рендерит шаблон страницы "Тарифы",
 - передает объекты из базы данных Tariffs.
"""


def tariffs_views(request):
    logger.info("Доступ к странице с тарифами.")
    tariffs = Tariffs.objects.all()
    context = {'tariffs': tariffs, }
    return render(request, 'gvk_site/tariffs_page.html', context)


"""
Представление страницы Качество воды:
 - рендерит шаблон страницы "Качество воды",
 - передает объекты из базы данных Quality.
"""


def quality_views(request):
    logger.info("Доступ к странице качества воды.")
    qualities = Quality.objects.all()
    context = {'qualities': qualities}
    return render(request, 'gvk_site/quality_page.html', context)


"""
Представление страницы Контакты:
 - рендерит шаблон страницы "Контакты".
"""


def contacts_views(request):
    logger.info("Доступ к странице контактов.")
    return render(request, 'gvk_site/contacts_page.html')


"""
Представление страницы Авторизация:
 - проверяет метод HTTP-запроса,
 - создает экземпляр формы LoginForm с данными, переданными через POST-запрос,
 - проверяет корректность формы, извлекает очищенные данные из формы,
 - ищет в базе данных пользователя по логину, если находит, то проверяет пароль и перенаправляет 
 на страницу личного кабинета,
 - генерирует исключение в случае отсутствия пользователя в базе,
 - рендерит шаблон страницы "Авторизация".

"""


def login_view(request):
    logger.info("Доступ к странице авторизации абонента.")
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
                logger.info("Введен неверный логин.")
                return render(request, 'gvk_site/login.html', context)

            logger.debug(f"Введенный пароль: {password}")
            logger.debug(f"Хранящийся пароль: {subscriber.password}")

            # Проверка пароля
            if check_password(password, subscriber.password):
                request.session['subscriber_id'] = subscriber.id
                logger.info("Введен верный пароль.")
                # Переход на страницу личного кабинета
                return redirect('personal_cabinet', pk=subscriber.pk)
            else:
                context = {'form': form, 'error_message': 'Неверный логин или пароль'}
                logger.info("Введен неверный пароль.")
                return render(request, 'gvk_site/login.html', context)

        else:
            logger.error("Форма невалидна: %s", form.errors)  # Логируем ошибки формы
    else:
        form = LoginForm()

    return render(request, 'gvk_site/login.html', {'form': form})


def employee_view(request):
    logger.info("Доступ к странице авторизации сотрудника.")
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.info(f"Форма валидна. Пользователь: {username}")

            try:
                employee = Employee.objects.get(name=username)
            except Employee.DoesNotExist:
                context = {'form': form, 'error_message': 'Неверный логин или пароль'}
                logger.info("Введен неверный логин.")
                return render(request, 'gvk_site/employee_login.html', context)

            logger.debug(f"Введенный пароль: {password}")
            logger.debug(f"Хранящийся пароль: {employee.password}")

            # Проверка пароля
            if check_password(password, employee.password):
                request.session['employee_id'] = employee.id
                logger.info("Введен верный пароль.")
                # Переход на страницу личного кабинета
                return redirect('years')
            else:
                context = {'form': form, 'error_message': 'Неверный логин или пароль'}
                logger.info("Введен неверный пароль.")
                return render(request, 'gvk_site/employee_login.html', context)

        else:
            logger.error("Форма невалидна: %s", form.errors)  # Логируем ошибки формы
    else:
        form = EmployeeLoginForm()

    return render(request, 'gvk_site/employee_login.html', {'form': form})
"""
Представление страницы Личный кабинет:
 - передает на страницу отдельные объекты из базы данных Subscribers с соответствующим id,
 - рендерит шаблон страницы "Личный кабинет". 
"""


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
        'previous_reading': subscriber.previous_reading,
        'current_reading': subscriber.current_reading
    }
    if request.method == 'POST':
        current_reading = request.POST.get('current_reading')

        # Проверяем, что поле current_reading не пустое
        if current_reading:
            try:
                current_reading_value = float(current_reading)
            except ValueError:
                logger.error("Невозможно преобразовать текущее показание в число.")
            else:
                subscriber.previous_reading = subscriber.current_reading
                subscriber.current_reading = current_reading_value
                subscriber.save(update_fields=['current_reading', 'previous_reading'])
                logger.info("Изменение текущего показания водосчетчика.")

    return render(request, 'gvk_site/personal_cabinet.html', context)


"""
Представление для выхода из личного кабинета:
- осуществляет выход пользователя из личного кабинета и перенаправляет на Главную страницу
"""


def logout_view(request):
    # Запись лога
    logger.info("Выход из личного кабинета")
    # Выход пользователя
    logout(request)
    # Перенаправление на главную страницу
    return redirect('home')


"""Представление для расчета сумм оплаты по воде и канализации
    и формирования квитанции в формате PDF с QR-кодом"""


def generate_invoice(request, pk):
    """Запросы к базе данных"""
    subscriber = get_object_or_404(Subscribers, pk=pk)
    tariffs = Tariffs.objects.first()
    address_str = str(subscriber.address)

    """Производится расчет суммы
    - вычисляется объем потребленной воды (текуще показания водосчетчика - предыдущие показания водосчетчика,
    - определяются населенный пункт проживания абонента: если "Пушной" 
    то расчет суммы производится с тарифом для данного населенного пункта,
    - если не "Пушной", то определяются имеющиеся виды услуг для данного абонента: только водоснабжение, 
    только водоотведение или водоснабжение и водоотведение,
    - в производится умножение объема на тариф соответствующих видов услуг,
    - определяется сумма по всем услугам"""
    if "Пушной" in address_str:
        water_sum = round(((subscriber.current_reading - subscriber.previous_reading) * float(tariffs.water_push)), 2)
        sewer_sum = 0
    elif subscriber.service_flag == 1:
        water_sum = round(((subscriber.current_reading - subscriber.previous_reading) * float(tariffs.water_ch)), 2)
        sewer_sum = 0
    elif subscriber.service_flag == 2:
        water_sum = round(((subscriber.current_reading - subscriber.previous_reading) * float(tariffs.water_ch)), 2)
        sewer_sum = round(((subscriber.current_reading - subscriber.previous_reading) * float(tariffs.sewerage)), 2)
    elif subscriber.service_flag == 3:
        water_sum = 0
        sewer_sum = round(((subscriber.current_reading - subscriber.previous_reading) * float(tariffs.sewerage)), 2)
    else:
        water_sum = 0
        sewer_sum = 0

    total_sum = water_sum + sewer_sum
    consumed_volume = subscriber.current_reading - subscriber.previous_reading

    """Создание квитанции об оплате в формате PDF"""
    logger.info("Формирование квитанции об оплате")
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('FreeSans', r'C:\Users\evgen\Diplom_Project\diplom_project\fonts\FreeSans.ttf'))
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('FreeSans', 18)
    p.setFillColor(colors.lightgrey)
    p.rect(102, 757, 400, 17, fill=1)
    p.setFillColor(colors.black)

    p.drawString(100, 800, f"Квитанция на оплату для абонента {subscriber.name}")
    p.drawString(100, 780, f"Адрес: {subscriber.address}")
    p.drawString(100, 760, "  Описание")
    p.drawString(350, 760, " | Сумма")
    p.drawString(100, 740, f"Потребленный объем воды: ")
    p.drawString(350, 740, f" | {consumed_volume}")
    p.drawString(100, 720, f"Сумма по водоснабжению: ")
    p.drawString(350, 720, f" | {water_sum}")
    p.drawString(100, 700, f"Сумма по водоотведению: ")
    p.drawString(350, 700, f" | {sewer_sum}")
    p.drawString(100, 680, f"ВСЕГО сумма: ")
    p.drawString(350, 680, f" | {total_sum}")
    p.drawString(100, 670, f"-------------------------------------------------------------------")

    """Генерация QR-кода"""
    qr = qrcode.make(f"Оплата: {total_sum}")
    qr_path = "qr_code.png"
    qr.save(qr_path)
    p.drawImage(qr_path, 100, 560, width=100, height=100)

    p.showPage()
    p.save()
    buffer.seek(0)

    """Возврат PDF как ответа"""
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Квитанция.pdf"'
    return response


"""Представление для страницы выбора отчетного года:
 - отображает ссылки для перенаправления на страницу с данными по выбранному году"""


def year_view(request):
    logger.info("Вход на страницу выбора отчетного года")
    years = [year[0] for year in YEAR_CHOICES]
    context = {'years': years}
    return render(request, 'gvk_site/year_page.html', context)

"""Представление для страницы выбора отчетного месяца и таблицы годового итога 
по водоснабжению или водоотведению
 - отображает ссылки для перенаправления на страницу с таблицами значений по отчетному месяцу или по году"""


def year_detail(request, year):
    logger.info("Вход на страницу выбора месяца отчетных работ.")
    monthworks = MonthWorks.objects.filter(year=year)
    watertable = WaterTable.objects.filter(year=year)
    severagetable = SeverageTable.objects.filter(year=year)
    context = {
        'year': year,
        'monthworks': monthworks,
        'watertable': watertable,
        'severagetable': severagetable
    }
    return render(request, 'gvk_site/year_detail.html', context)


"""Представление для отображения страницы с таблицей работ по выбранному месяцу"""


def monthworks_list(request, year, month):
    works = MonthWorks.objects.filter(year=year, month=month)
    logger.info(f"Вход на страницу с работами за {dict(MonthWorks.MONTH_CHOICES)[month]} {year} года")
    context = {
        'works': works,
        'month_name': dict(MonthWorks.MONTH_CHOICES)[month]
    }
    return render(request, 'gvk_site/monthworks_list.html', context)


"""Представление для отображения страницы с суммарной таблицей годовых работ по водоснабжению"""


def watertable_view(request, year):
    try:
        watertables = WaterTable.objects.filter(year=year)
        logger.info(f"Доступ к таблице ремонтов по водоснабжению за  {year} год")
    except Exception as e:
        return HttpResponse(e)
    context = {
        'watertables': watertables,
        'year': year}
    return render(request, 'gvk_site/watertable.html', context)


"""Представление для отображения страницы с суммарной таблицей годовых работ по водотведению"""


def severagetable_view(request, year):
    try:
        severagetables = SeverageTable.objects.filter(year=year)
        logger.info(f"Доступ к таблице ремонтов по водоотведению за  {year} год")
    except Exception as e:
        return HttpResponse(e)
    context = {'severagetables': severagetables,
               'year': year}
    return render(request, 'gvk_site/severagetable.html', context)