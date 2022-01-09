"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
import vacancies.views as vacancies
from login.views import MySignupView, MyLoginView
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static


handler404 = vacancies.custom_handler404

handler500 = vacancies.custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vacancies.main_view),
    path('companies', vacancies.companies, name='companies'),

    path('vacancies', vacancies.vacancies, name='vacancies'),
    path('vacancies/', include([
        path('<str:category_name>', vacancies.vacancies_on_category, name='vacancies_on_category'),
        path('cat/<str:category_name>', vacancies.vacancies_on_category, name='vacancies_on_category'),
        path('companies/<int:company>', vacancies.company_card, name='company_card'),
        path('<int:vacancy_id>/send', vacancies.send_application, name='send_application'),
    ])),
    path('vacancy/<int:vacancy_id>', vacancies.vacancy, name='vacancy'),

    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view()),

    path('mycompany', vacancies.mycompany, name='mycompany'),
    path('mycompany/', include([
        path('start_company', vacancies.start_company, name='start_company'),
        path('create_company', vacancies.create_company, name='create_company'),
        path('create_vacancy', vacancies.create_vacancy, name='create_vacancy'),
        path('vacancies', vacancies.my_vacancies, name='my_vacancies'),
        path('edit_vacancy/<int:vacancy>', vacancies.edit_vacancy, name='edit_vacancy'),
    ])),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
