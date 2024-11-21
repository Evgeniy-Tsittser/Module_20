from django.urls import path
from .views import (home_views, about_views, tariffs_views, quality_views,
                    contacts_views, login_view, personal_cabinet_view)

urlpatterns = [
    path('', home_views, name='home'),
    path('about/', about_views, name='about'),
    path('tariffs/', tariffs_views, name='tariffs'),
    path('quality/', quality_views, name='quality'),
    path('contacts/', contacts_views, name='contacts'),
    path('login/', login_view, name='login'),
    path('personal_cabinet/<int:pk>/', personal_cabinet_view, name='personal_cabinet'),
]
