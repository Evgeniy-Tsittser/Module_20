import os
import django
from django.test import TestCase, Client
from django.urls import reverse
from .models import Tariffs, Quality, Subscribers, Address
from django.contrib.auth.hashers import make_password
from .forms import LoginForm
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()


# Тестируем представление домашней страницы
class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        # Тестируем статус-код ответа
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        # Проверяем использование правильного шаблона
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'gvk_site/home_page.html')


# Тестируем представление страницы О предприятии
class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_view_status_code(self):
        # Тестируем статус-код ответа
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template_used(self):
        # Проверяем использование правильного шаблона
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'gvk_site/about_page.html')


# Тестируем представление страницы тарифов
class TariffViewsTest(TestCase):
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


# Тестируем представление страницы качества воды
class QualityViewsTest(TestCase):
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


# Тестируем представление страницы контактов
class ContactsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contacts_view_status_code(self):
        # Тестируем статус-код ответа
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_template_used(self):
        # Проверяем использование правильного шаблона
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'gvk_site/contacts_page.html')


# Тестируем представление страницы авторизации
class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
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


# Тестируем представление страницы личного кабинета
class PersonalCabinetViewTests(TestCase):

    def setUp(self):
        self.client = Client()
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

        # Проверяем, что статус ответа 200
        self.assertEqual(response.status_code, 200)
        # Проверяем, что контекст включает отправляемые данные
        self.assertContains(response, f'Приветствую, {self.subscriber.name}')

    def test_personal_cabinet_view_not_found(self):
        """Тестируем доступ к личному кабинету с несуществующим pk."""
        self.client.login(name='test_user', password='test_password')  # Логиним пользователя
        response = self.client.get(reverse('personal_cabinet', args=[999]))  # 999 - несуществующий pk

        logger.info("Response status code for not found: %d", response.status_code)

        # Проверяем, что вызывается 404 ошибка
        self.assertEqual(response.status_code, 404)
