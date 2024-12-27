from django.test import TestCase, Client
from django.core.cache import cache
from django.urls import reverse
from gvk_site.models import MonthWorks, WaterTable, SeverageTable, YEAR_CHOICES
from gvk_site.views import year_view, year_detail, monthworks_list, severagetable_view

"""Тест представления year_view"""


class YearViewTest(TestCase):
    def setUp(self):
        """Чистим кэш"""
        cache.clear()
        """Подключаем тестовый сервер перед вызовом каждой функции"""
        self.client = Client()

    def test_year_view_status_code(self):
        """Проверяем, что представление возвращает код состояния 200"""
        response = self.client.get(reverse('years'))
        self.assertEqual(response.status_code, 200)

    def test_year_view_context_data(self):
        """Проверяем наличие ключа 'years' в контексте данных.
        Сравниваем список лет из контекста с ожидаемым списком лет"""
        response = self.client.get(reverse('years'))
        self.assertIn('years', response.context)
        expected_years = [year[0] for year in YEAR_CHOICES]
        self.assertListEqual(list(response.context['years']), expected_years)


"""Тест представления year_detail"""


class YearDetailViewTest(TestCase):

    def setUp(self):
        """Чистим кэш"""
        cache.clear()
        """Создаем временную тестовую базу данных"""
        self.year = 2021
        self.monthwork_1 = MonthWorks.objects.create(
            year=self.year,
            type_work=3,
            month=4)
        self.watertable_1 = WaterTable.objects.create(
            year=self.year)
        self.severagetable_1 = SeverageTable.objects.create(
            year=self.year)
        """Подключаем тестовый сервер перед вызовом каждой функции"""
        self.client = Client()

    def test_year_detail_view_status_code(self):
        """Проверяем, что представление возвращает код состояния 200"""
        url = reverse('year_detail', args=[self.year])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_year_detail_view_context_data(self):
        """Проверяем, что представление правильно передает данные в контекст"""
        url = reverse('year_detail', args=[self.year])
        response = self.client.get(url)
        self.assertContains(response, str(self.year))
        """Извлекаем значения из контекста представления, преобразуем их в строковые значения 
        и создаем из них список"""
        monthworks_values = list(map(repr, response.context['monthworks']))
        watertable_values = list(map(repr, response.context['watertable']))
        severagetable_values = list(map(repr, response.context['severagetable']))

        """Сравниваем полученные списки значений с ожидаемыми значениями"""
        self.assertSequenceEqual(monthworks_values, [repr(self.monthwork_1)])
        self.assertSequenceEqual(watertable_values, [repr(self.watertable_1)])
        self.assertSequenceEqual(severagetable_values, [repr(self.severagetable_1)])


"""Тест представления monthworks_list"""


class MonthWorksListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Чистим кэш"""
        cache.clear()
        """Создаем временную тестовую базу данных"""
        cls.year = 2020
        cls.month = 10
        cls.work_1 = MonthWorks.objects.create(
            year=cls.year,
            month=cls.month,
            type_work=1,
        )

    def setUp(self):
        """Подключаем тестовый сервер перед вызовом каждой функции"""
        self.client = Client()

    def test_monthworks_list_view_status_code(self):
        """Проверяем, что представление возвращает код состояния 200"""
        url = reverse('monthworks_list', args=[self.year, self.month])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_monthworks_list_view_context_data(self):
        """Проверяем, что представление правильно передает данные в контекст"""
        url = reverse('monthworks_list', args=[self.year, self.month])
        response = self.client.get(url)
        self.assertEqual(response.context['month_name'], 'Октябрь')
        self.assertQuerySetEqual(response.context['works'], MonthWorks.objects.filter(year=self.year, month=self.month),
                                 transform=lambda x: x)


"""Тест представления watertable_view"""


class WaterTableViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Чистим кэш"""
        cache.clear()
        """Создаем временную тестовую базу данных"""
        cls.year = 2024
        cls.water_table_2 = WaterTable.objects.create(year=cls.year, completed_works="Sample data 1")
        cls.water_table_3 = WaterTable.objects.create(year=cls.year, completed_works="Sample data 2")
        cls.invalid_year = 9999  # Год, для которого нет записей

    def setUp(self):
        """Подключаем тестовый сервер перед вызовом каждой функции"""
        self.client = Client()

    def test_watertable_view_with_valid_year(self):
        """Проверяем, что представление правильно отображает данные, когда передан корректный год"""
        url = reverse('watertable', args=[self.year])
        response = self.client.get(url)

        """Проверяем статус ответа"""
        self.assertEqual(response.status_code, 200)

        """Проверяем контекст"""
        self.assertIn('watertables', response.context)
        self.assertQuerySetEqual(
            response.context['watertables'].order_by('id'),
            WaterTable.objects.filter(year=self.year).order_by('id'),
            transform=lambda x: x
        )

        """Проверяем, что год в контексте соответствует ожидаемому"""
        self.assertEqual(response.context['year'], self.year)

        """Проверяем, что используется правильный шаблон"""
        self.assertTemplateUsed(response, 'gvk_site/watertable.html')

    def test_watertable_view_with_invalid_year(self):
        """Получаем URL для нашего представления с недоступным годом"""
        url = reverse('watertable', args=[self.invalid_year])
        response = self.client.get(url)

        """Проверяем статус ответа"""
        self.assertEqual(response.status_code, 200)

        """Проверяем, что контекст 'watertables' пуст"""
        self.assertIn('watertables', response.context)
        self.assertQuerySetEqual(response.context['watertables'], [])  # Ожидание пустого списка

        """Проверяем, что год в контексте соответствует ожидаемому"""
        self.assertEqual(response.context['year'], self.invalid_year)

    def test_watertable_view_exception_handling(self):
        """Временное удаление всех объектов WaterTable для проверки обработки исключений"""
        WaterTable.objects.all().delete()
        url = reverse('watertable', args=[self.year])
        response = self.client.get(url)

        """Проверяем, что контекст 'watertables' пуст"""
        self.assertIn('watertables', response.context)
        self.assertQuerySetEqual(response.context['watertables'], [])  # Ожидание пустого списка

        """Проверяем, что год в контексте соответствует ожидаемому"""
        self.assertEqual(response.context['year'], self.year)


"""Тест представления severagetable_view"""


class SewerageTableViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Чистим кэш"""
        cache.clear()
        """Создаем временную тестовую базу данных"""
        cls.client = Client()
        cls.year = 2024
        cls.severage_table_entry = SeverageTable.objects.create(year=cls.year, completed_works="Sample data")
        cls.invalid_year = 9999

    def test_severagetable_view_with_valid_year(self):
        """Проверяем, что представление правильно отображает данные, когда передан корректный год"""
        url = reverse('severagetable', args=[self.year])
        response = self.client.get(url)
        """Проверяем статус ответа"""
        self.assertEqual(response.status_code, 200)
        """Проверяем контекст"""
        self.assertIn('severagetables', response.context)
        self.assertQuerySetEqual(
            response.context['severagetables'],
            SeverageTable.objects.filter(year=self.year),
            transform=lambda x: x)

        """Проверяем, что год в контексте соответствует ожидаемому"""
        self.assertEqual(response.context['year'], self.year)
        """Проверяем, что используется правильный шаблон"""
        self.assertTemplateUsed(response, 'gvk_site/severagetable.html')

    def test_severagetable_view_with_invalid_year(self):
        """Проверяет, что представление возвращает пустой список для недоступного года."""
        url = reverse('severagetable', args=[self.invalid_year])
        response = self.client.get(url)
        """Проверяем статус ответа"""
        self.assertEqual(response.status_code, 200)
        """Проверяем контекст"""
        self.assertIn('severagetables', response.context)
        """Проверяем, что возвращаемый список пустой"""
        self.assertQuerySetEqual(response.context['severagetables'], [])
        """Проверяем, что год в контексте соответствует ожидаемому"""
        self.assertEqual(response.context['year'], self.invalid_year)
        """Проверяем, что используется правильный шаблон"""
        self.assertTemplateUsed(response, 'gvk_site/severagetable.html')

    def test_severagetable_view_exception_handling(self):
        """Проверяет обработку исключения в представлении
        Например, мы можем удалить все записи, чтобы увидеть, что вернется"""
        SeverageTable.objects.all().delete()

        """Вызываем представление, которое должно вернуть обработанное значение"""
        url = reverse('severagetable', args=[self.year])
        response = self.client.get(url)

    def test_severagetable_view_with_invalid_year_type(self):
        """Проверяет поведение представления, если передан год некорректного типа."""
        response = self.client.get(reverse('severagetable', args=[self.year]))
        """Изменение Url"""
        invalid_url = '/severage/invalid_year_type/'

        response = self.client.get(invalid_url)

        """Ожидаем 404, так как представление не должно принимать строку вместо года"""
        self.assertEqual(response.status_code, 404)