## **Описание проекта**

"Сайт ООО "Горводоканал"" — это веб-приложение для предоставления пользователям информации о деятельности предприятия, а также возможностью 
создания базы данных об абонентах, их приборах учета. Посредством базы данных о приборах учета можно направлять СМС-уведомления абонентам о 
необходимости провести очередную поверку прибора учета воды. В разделе для сотрудников организации имеется возможность получать информацию 
о проведенных ремонтных работах, их объемах и стоимости. Входы в личный кабинеты абонента и сотрудников осуществляются через соответствующие 
формы авторизации.

## **Основные особенности:**

- **Регистрация** пользователей.
- Возможность добавления, редактирования и удаления данных об абонентах и их приборах учета администратором приложения.
- **Регистрация** сотрудников.
- - Возможность добавления, редактирования и удаления сотрудников администратором приложения.
- **Авторизация** пользователей.
- При регистрации абонента ему присваивается логин и пароль, посредством которых он может посещать личный кабинет.
- Применен функционал автоматического отслеживания наступления определенного периода до наступления даты окончания срока поверки
  приборов учета и направления СМС-уведомления абоненту.
- Имеется возможность вносить абонентом текущие показание прибора учета и формировать квитанцию об оплате в PDF-формате с QR-кодом.
- **Авторизация** ссотрудников.
- При регистрации сотрудника ему присваивается логин и пароль, посредством которых он может посещать раздел для сотрудников.
- В разделе для сотрудников имеются таблицы с ремонтными работами с возможностью выбора таблиц по конкретному году и месяцу.
- Тестирование функций и логирование ошибок и событий для удобства отладки и мониторинга.

## **Технологии:**

- **Django** 5.1.3
- **PostgreSQL** (база данных)
- **Celery**  (для работы с автоматическими задачами)
- **RabbitMQ** (брокер для задач)
- **SMSAero** (Сервис для отправки SMS-сообщений)
- **Python 3.12**
- **Signals**  (для работы с синхронным изменением данных в таблицах)
- **Reportlab**  (для формирования документа в PDF-формате)
- **Qrcode**  (для генерации qr-кода)

## **Зависимости**
```bash
Для работы проекта требуется установить зависимости, приведенные в файле:
- requirements.txt
```
## **Установка и запуск проекта**

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Evgeniy-Tsittser/Module_20.git                                    
перейдите в директорию проекта cd diplom_project
```
### 2. Создайте виртуальное окружение и активируйте его
```bash
python -m venv myenv
source myenv/bin/activate   # для Linux/MacOS
myenv\Scripts\activate      # для Windows
```
### 3. Установите зависимости
```bash
pip install -r requirements.txt
```
###  4. Примените миграции базы данных
```bash
python manage.py migrate
```
### 5. Создайте суперпользователя для доступа к админ-панели
```bash
python manage.py createsuperuser
```
### 6. Запустите сервер
```bash
python manage.py runserver
```
Теперь проект доступен по адресу: http://127.0.0.1:8000/.

## Структура проекта
![Структура](https://github.com/user-attachments/assets/cec45c4e-5b28-425e-9ac1-6c132b3fbc46)

## Использование
1. Если вы администратор, то для добавления данных в базы данных перейдите по ссылке http://127.0.0.1:8000/admin.
2. Выберите необходимую базу и внесите данные.
3. Добавленные или измененные данные будут отображаться на соответствующих страницах приложения, которые доступны по ссылкам на Главной странице.
4. Если вы абонент, то в правой панели Главной страницы перейдите по ссылке "Авторизация абонента". Введите логин и пароль и перейдите в личный
 кабинет. Логин и пароль можно получить у администратора при регистрации.
5. Если вы сотрудник, то в правой панели Главной страницы перейдите по ссылке "Ремонтные работы". Введите логин и пароль и перейдите на страницу
выбора года ремонтных работ. Логин и пароль можно получить у администратора при регистрации.

## Демонстрация работы приложения представлена изображениями:
    - Главная страница:
  ![Главная](https://github.com/user-attachments/assets/77e0e8c2-bb47-4260-997c-82a687af01bb)
 
    - Страница "О предприятии"
  ![О предприятии](https://github.com/user-attachments/assets/28aa91b2-2872-4167-9dc2-c2b60e4afac2)

    - Страница "Тарифы"
  ![Тарифы](https://github.com/user-attachments/assets/cc8a9ff4-2d85-4dfa-97da-587e38925e9b)

    - Страница "Контакты"
  ![Контакты](https://github.com/user-attachments/assets/344a9dee-cb11-4a28-b03b-4b22ac9d9047)

    - Страница "Качество воды"
  ![Качество](https://github.com/user-attachments/assets/92238b40-761c-4eec-91e7-b4711facf2e8)

    - Страница авторизации абонента
  ![Авторизация абонента](https://github.com/user-attachments/assets/309d7b5c-0475-439b-b5f7-35bb136676f7)

    - Страница личного кабинета абонента
  ![Личный кабинет](https://github.com/user-attachments/assets/26a22572-2036-4303-b687-4b4ce896ed6a)

    - Страница авторизации сотрудника
  ![Авторизация сотрудника](https://github.com/user-attachments/assets/7948c518-c5ad-4c0a-b12e-d5b3e726348b)

    - Страница выбора года ремонтных работ
  ![ВЫбор года](https://github.com/user-attachments/assets/aa1cbd5f-e7e3-4c1a-b791-e54aaf265e5e)

    - Страница выбора таблиц ремонтных работ
  ![Выбор таблиц](https://github.com/user-attachments/assets/6c26eb28-9d9a-4a9a-ae98-74c75ba19d0e)

    - Страница работ за выбранный месяц
  ![Меячные работы](https://github.com/user-attachments/assets/618dc049-8092-44a6-9ea1-0a64912d6053)

    - Страница годовых работ по водоснабжению
  ![Годовая водоснабжение](https://github.com/user-attachments/assets/cf05725c-f4eb-40dd-bc84-e44bc9a12168)

    - Страница годовых работ по водоотведению
  ![Годовая водоотведение](https://github.com/user-attachments/assets/601a93af-8056-4b45-8018-9c6711b4b295)

    - Админ-панель
  ![Админка](https://github.com/user-attachments/assets/68f99092-4a31-4608-970b-513e4f9207a3)
    
## Тестирование и Логирование
```bash
1. Для тестирования функций представления приложения откройте терминал.
2. Перейдите в директорию проекта cd diplom_project.
3. Для тестирования представлений общедоступной части приложения, авторизацию и личный кабинет, то необходимо набрать
в командной строке: python manage.py test gvk_site.tests.gvk_site_tests.tests.
4. Для тестирования представлений части приложения с таблицами ремонтных работ, то необходимо набрать в командной
строке: python manage.py test gvk_site.tests.rembaza_tests.test. 
```
4. Логирование осуществляется через стандартные механизмы Django. Все ошибки записываются в файл django.log
