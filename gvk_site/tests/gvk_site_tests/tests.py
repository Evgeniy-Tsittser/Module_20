import os
import django
from django.test import TestCase, Client
from django.urls import reverse
from gvk_site.models import Tariffs, Quality, Subscribers, Address, Employee
from django.contrib.auth.hashers import make_password
from gvk_site.forms import LoginForm, EmployeeLoginForm
from io import BytesIO
from PyPDF2 import PdfReader
from email.header import decode_header
import logging

"""Подключение логирования для тестов."""
logger = logging.getLogger(__name__)

"""Настройки окружения Джанго для тестов"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diplom_project.settings")
django.setup()

"""Класс тестирования Главной страницы."""


class HomeViewTest(TestCase):

    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()

    def test_home_view_status_code(self):
        """Тестируем статус-код ответа"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """Проверяем использование правильного шаблона"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'gvk_site/home_page.html')


"""Класс тестирования представления страницы О предприятии"""


class AboutViewTest(TestCase):

    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()

    def test_about_view_status_code(self):
        """Тестируем статус-код ответа"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template_used(self):
        """Проверяем использование правильного шаблона"""
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'gvk_site/about_page.html')


"""Класс тестирования представления страницы Тарифы"""


class TariffViewsTest(TestCase):
    """Создаем тестовую базу данных"""

    @classmethod
    def setUpTestData(cls):
        cls.tariff_1 = Tariffs.objects.create(water_ch=45, water_push=35, sewerage=39)
        cls.tariff_2 = Tariffs.objects.create(water_ch=50, water_push=40, sewerage=46)

    def test_tariffs_view_status_code(self):
        """Тестируем статус-код ответа"""
        response = self.client.get(reverse('tariffs'))
        self.assertEqual(response.status_code, 200)

    def test_tariffs_view_template_used(self):
        """Проверяем использование правильного шаблона"""
        response = self.client.get(reverse('tariffs'))
        self.assertTemplateUsed(response, 'gvk_site/tariffs_page.html')

    def test_tariffs_view_context_data(self):
        """Проверяем наличие контекста данных"""
        response = self.client.get(reverse('tariffs'))
        self.assertIn('tariffs', response.context)
        self.assertCountEqual(
            response.context['tariffs'],
            [self.tariff_1, self.tariff_2]
        )


"""Класс тестирования представления страницы Качество воды"""


class QualityViewsTest(TestCase):
    """Создаем тестовую базу данных"""

    @classmethod
    def setUpTestData(cls):
        cls.quality_1 = Quality.objects.create(month=45, iron=35, manganese=39, turbidity=55, rigidity=2)
        cls.quality_2 = Quality.objects.create(month=50, iron=40, manganese=46, turbidity=56, rigidity=3)

    def test_quality_view_status_code(self):
        """Тестируем статус-код ответа"""
        response = self.client.get(reverse('quality'))
        self.assertEqual(response.status_code, 200)

    def test_quality_view_template_used(self):
        """Проверяем использование правильного шаблона"""
        response = self.client.get(reverse('quality'))
        self.assertTemplateUsed(response, 'gvk_site/quality_page.html')

    def test_quality_view_context_data(self):
        """Проверяем наличие контекста данных"""
        response = self.client.get(reverse('quality'))
        self.assertIn('qualities', response.context)
        self.assertCountEqual(
            response.context['qualities'],
            [self.quality_1, self.quality_2]
        )


"""Класс тестирования представления страницы Контакты"""


class ContactsViewTest(TestCase):
    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()

    def test_contacts_view_status_code(self):
        """Тестируем статус-код ответа"""
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_template_used(self):
        """Проверяем использование правильного шаблона"""
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'gvk_site/contacts_page.html')


"""Класс тестирования представления страницы Авторизации"""


class LoginViewTest(TestCase):

    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()
        """Создаем тестовую базу данных"""
        self.address = Address.objects.create(address="Test Address")
        self.subscriber = Subscribers.objects.create(
            address=self.address,
            login="test_user",
            password="test_password",
            damage_data="2023-01-01",
            verifi_period="2023-12-31"
        )

    def test_login_get_request(self):
        """Тестируем GET-запрос к странице авторизации."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gvk_site/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_successful_login(self):
        """Тестируем успешную аутентификацию."""
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(reverse('login'), data=data)
        logger.info("Response status code: %d", response.status_code)
        logger.info("Response content: %s", response.content.decode())
        self.assertRedirects(response, reverse('personal_cabinet', args=[self.subscriber.pk]))
        self.assertTrue(self.client.session.get('subscriber_id'))

    def test_invalid_credentials(self):
        """Тестируем попытку входа с неверным логином или паролем."""
        data = {
            'username': 'wrong_username',
            'password': 'wrong_password'
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')
        self.assertFalse(self.client.session.get('subscriber_id'))

    def test_missing_subscriber(self):
        """Тестируем попытку входа с несуществующим пользователем."""
        data = {
            'username': 'nonexistent_user',
            'password': 'any_password'
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')
        self.assertFalse(self.client.session.get('subscriber_id'))


"""Класс тестирования представления страницы Личного кабинета"""


class PersonalCabinetViewTests(TestCase):

    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()
        """Создаем тестовую базу данных"""
        self.address = Address.objects.create(address="Test Address")
        self.subscriber = Subscribers.objects.create(
            address=self.address,
            name="test_user",
            password=make_password("test_password"),
            damage_data="2023-01-01",
            verifi_period="2023-12-31"
        )

    def test_personal_cabinet_view_success(self):
        """Тестируем доступ к личному кабинету с валидным pk."""
        self.client.login(name='test_user', password='test_password')  # Логиним пользователя
        response = self.client.get(reverse('personal_cabinet', args=[self.subscriber.pk]))

        logger.info("Response status code: %d", response.status_code)
        logger.info("Response content: %s", response.content.decode())

        """Проверяем, что статус ответа 200"""
        self.assertEqual(response.status_code, 200)
        # Проверяем, что контекст включает отправляемые данные
        self.assertContains(response, f'Приветствую, {self.subscriber.name}')

    def test_personal_cabinet_view_not_found(self):
        """Тестируем доступ к личному кабинету с несуществующим pk."""
        self.client.login(name='test_user', password='test_password')  # Логиним пользователя
        response = self.client.get(reverse('personal_cabinet', args=[999]))  # 999 - несуществующий pk

        logger.info("Response status code for not found: %d", response.status_code)

        """Проверяем, что вызывается 404 ошибка"""
        self.assertEqual(response.status_code, 404)


class EmployeeViewTest(TestCase):

    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()
        """Создаем тестовую базу данных"""
        self.employee = Employee.objects.create(
            name="test_user",
            password="test_password",
        )

    def test_login_get_request(self):
        """Тестируем GET-запрос к странице авторизации."""
        response = self.client.get(reverse('employee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gvk_site/employee_login.html')
        self.assertIsInstance(response.context['form'], EmployeeLoginForm)

    def test_successful_login(self):
        """Тестируем успешную аутентификацию."""
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(reverse('employee'), data=data)
        logger.info("Response status code: %d", response.status_code)
        logger.info("Response content: %s", response.content.decode())
        self.assertRedirects(response, reverse('years'))
        self.assertTrue(self.client.session.get('employee_id'))

    def test_invalid_credentials(self):
        """Тестируем попытку входа с неверным логином или паролем."""
        data = {
            'username': 'wrong_username',
            'password': 'wrong_password'
        }
        response = self.client.post(reverse('employee'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')
        self.assertFalse(self.client.session.get('employee_id'))

    def test_missing_subscriber(self):
        """Тестируем попытку входа с несуществующим пользователем."""
        data = {
            'username': 'nonexistent_user',
            'password': 'any_password'
        }
        response = self.client.post(reverse('employee'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')
        self.assertFalse(self.client.session.get('employee_id'))


class InvoiceGenerationTest(TestCase):
    """Тестируем представление формирования квитанции"""
    def setUp(self):
        """Подключение тестового сервера"""
        self.client = Client()

        """Создаем тестовую базу данных"""
        self.address = Address.objects.create(address="ул. Пушкина, д. 10")
        self.tariff = Tariffs.objects.create(water_push=20, water_ch=15, sewerage=10)
        self.subscriber = Subscribers.objects.create(
            name="Иван Иванов",
            address=self.address,
            damage_data="2023-10-12",
            verifi_period="2024-10-12",
            current_reading=50,
            previous_reading=30,
            service_flag=2
        )

    def test_generate_invoice(self):
        """Отправляем GET запрос на генерацию счета"""
        response = self.client.get(f'/generate_invoice/{self.subscriber.pk}/')

        """Проверяем, что статус ответа 200"""
        self.assertEqual(response.status_code, 200)

        """Проверяем тип контента"""
        self.assertEqual(response['Content-Type'], 'application/pdf')

        """Получаем заголовок"""
        content_disposition = response['Content-Disposition']
        # Декодируем заголовок
        decoded_content_disposition = decode_header(content_disposition)[0][0].decode('utf-8')

        """Проверяем наличие заголовка"""
        self.assertIn('Content-Disposition', response)
        self.assertEqual(decoded_content_disposition, 'inline; filename="Квитанция.pdf"')

        """Проверяем, что тело ответа содержит действительный PDF документ"""
        try:
            num_pages = len(PdfReader(BytesIO(response.content)).pages)
        except Exception as e:
            self.fail("Не удалось прочитать PDF файл.")