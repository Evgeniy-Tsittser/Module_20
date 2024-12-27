from django.urls import path
from .views import (home_views, about_views, tariffs_views, quality_views,
                    contacts_views, login_view, personal_cabinet_view,
                    logout_view, generate_invoice, employee_view, year_view,
                    year_detail, monthworks_list, watertable_view, severagetable_view)

urlpatterns = [
    path('', home_views, name='home'),
    path('about/', about_views, name='about'),
    path('tariffs/', tariffs_views, name='tariffs'),
    path('quality/', quality_views, name='quality'),
    path('contacts/', contacts_views, name='contacts'),
    path('login/', login_view, name='login'),
    path('personal_cabinet/<int:pk>/', personal_cabinet_view, name='personal_cabinet'),
    path('logout/', logout_view, name='logout'),
    path('generate_invoice/<int:pk>/', generate_invoice, name='generate_invoice'),
    path('employee_login/', employee_view, name='employee'),
    path('years/', year_view, name='years'),
    path('year_detail/<int:year>', year_detail, name='year_detail'),
    path('month/<int:year>/<int:month>/', monthworks_list, name='monthworks_list'),
    path('water/<int:year>/', watertable_view, name='watertable'),
    path('severage/<int:year>', severagetable_view, name='severagetable'),
]
