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
import vacancies.views as vacancies
from vacancies.views import MySignupView, MyLoginView
from  django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static


handler404 = vacancies.custom_handler404

handler500 = vacancies.custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vacancies.main_view),
    path('vacancies', vacancies.vacancies, name='vacancies'),
    path('vacancies/cat/<str:category_name>', vacancies.vacancies_on_category, name='vacancies_on_category'),
    path('vacancies/companies/<int:company>', vacancies.company_card, name='company_card'),
    path('vacancies/<int:vacancy>', vacancies.vacancy, name='vacancy'),
    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)