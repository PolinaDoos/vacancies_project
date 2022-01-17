from typing import Any, Dict
from django.contrib import messages
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from vacancies.models import Application, Company, Specialty, Vacancy
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required
import random

from .forms import ApplicationForm, CompanyForm, VacancyForm

# для работы с запросами в shell: 
# import django.contrib.auth.models as auth - auth.User.objects.all()
# import vacancies.models as models -> models.Company.objects.all()

def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Или ничего нет. Простите, извините!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не отвечает именно Вам')


def main_view(request):
    company_vacancies = Company.objects.annotate(vacancies_count=Count('companies'))
    specialty_vacancies = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
    context = {
        'specialty_vacancies': specialty_vacancies,
        'company_vacancies': company_vacancies,
    }
    return render(request, 'index.html', context)

class MainView(ListView):
    # только модель, без фильтров
    model = Company
    
    # по умолчанию рендеринг шаблона app/templates/model_list.html
    template_name = "vacancies/index.html"

    # по умолчанию на шаблон передается переменная object_list = model.objects.all()
    context_object_name = 'company_vacancies' #- это данные Company.objects.all()

    # переопределяет queryset из Company.objects.all() в любой другой
    def get_queryset(self) -> QuerySet[Company]:
        # например, в этот. order_by('?')[:8] = 8 случайных
        queryset = Company.objects.annotate(vacancies_count=Count('companies')).order_by('?')[:8]
        return queryset


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['specialty_vacancies'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        return context


def vacancies(request):
    context = {
        'all_vacancies': Vacancy.objects.all(),
        'number_of_vacancies': len(Vacancy.objects.all())
    }
    return render(request, 'vacancies.html', context)


def companies(request):
    context = {
        'all_companies': Company.objects.all(),
        'number_of_companies': len(Company.objects.all())
    }
    return render(request, 'companies.html', context)


def vacancies_on_category(request, category_name):
    try:
        specialty = Specialty.objects.get(code=category_name)
        vacancies_on_category = Vacancy.objects.filter(specialty=specialty)
        context = {
            'vacancies_on_category': vacancies_on_category,
            'specialty': specialty,
            'number_of_vacancies': len(vacancies_on_category),
        }
        return render(request, 'vacancies_on_category.html', context)
    except Specialty.DoesNotExist or Vacancy.DoesNotExist:
        return redirect(main_view)


def company_card(request, company):
    try:
        company_data = Company.objects.get(id=company)
        vacancies_data = Vacancy.objects.filter(company=company_data.id)
        context = {
            'company_data': company_data,
            'vacancies_data': vacancies_data,
            'number_of_vacancies': len(vacancies_data),
        }
        return render(request, 'company_card.html', context)
    except Company.DoesNotExist or Vacancy.DoesNotExist:
        return redirect(main_view)


@login_required
def vacancy(request, vacancy_id):
    try:
        vacancy_data = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        return redirect(main_view)
    skills = vacancy_data.skills.split(",")
    form = ApplicationForm()

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = Vacancy.objects.get(id=vacancy_id)
            print(request.user)
            application.user = request.user

            # application.user is None if request.user == AnonymousUser else application.user = request.user
            # application.user = request.user if request.user else application.user is None
            application.save()
            return redirect ('send_application', vacancy_id)
        else:
            messages.error(request, 'Ошибка в заполнении формы')

    context = {
    'vacancy_data': vacancy_data,
    'skills': skills,
    'form': form,
    }
    return render(request, 'vacancy_card.html', context)
    

def send_application(request, vacancy_id):
    messages.success(request, 'Отклик отправлен')
    sender = Application.objects.filter(user=request.user).last().written_username
    context = {
        'vacancy_data': Vacancy.objects.get(id=vacancy_id),
        'sender': sender,
    }
    return render(request, 'send_application.html', context)


@login_required
def start_company(request):
    return render(request, 'start_company.html')


@login_required
def create_company(request):
    form = CompanyForm()
    if request.method == "POST":
        form= CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            messages.info(request, 'форма валидна')
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, f'{request.user.username}, карточка компании создана')
            return redirect(main_view)
        else:
            messages.error(request, 'Ошибка в заполнении формы')
        
    context = {
        'form': form,
    }
    return render(request, 'create_company.html', context)


@login_required
def mycompany(request):
    form = get_object_or_404(Company, owner=request.user)
    logo = form.logo
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены')
            return redirect('mycompany')
    else:
        form = CompanyForm(instance=form)
    context = {
        'form': form,
        'logo': logo
    }
    return render(request, 'mycompany.html', context)


@login_required
def my_vacancies(request):

    logo = get_object_or_404(Company, owner=request.user).logo
    try:
        user_vacancy_list = Vacancy.objects.filter(company=request.user.company)
        context = {
            'user_vacancy_list': user_vacancy_list,
            'logo': logo
        }
        return render(request, 'my_vacancies.html', context)
    except Vacancy.DoesNotExist:
        return redirect(mycompany)
    

@login_required
def create_vacancy(request):
    if request.method == "POST":
        form= VacancyForm(request.POST)
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            messages.error(request, 'Для публикации вакансии необходимо создать карточку компании')
            return redirect(create_company)
        published_at = datetime.today()
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company=company
            vacancy.published_at=published_at
            vacancy.save()
            messages.success(request, 'Вакансия опубликована')
            return redirect('my_vacancies')
        else:
            messages.error(request, 'Ошибка в заполнении формы')
    else:
        form = VacancyForm()
        
    context = {
        'form': form,
    }
    return render(request, 'create_vacancy.html', context)


@login_required
def edit_vacancy(request, vacancy):
    form = get_object_or_404(Vacancy, id=vacancy)
    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные вакансии обновлены')
            return redirect('my_vacancies')
    else:
        form = VacancyForm(instance=form)
    context = {
        'form': form,
    }
    return render(request, 'edit_vacancy.html', context)


class ApplicationList(ListView):
    model = Application
    template_name = "vacancies/applications.html"

    # по умолчанию на шаблон передается переменная object_list = model.objects.all()
    context_object_name = 'applications'

    def get_queryset(self):                                      
        vacancy = self.kwargs.get('vacancy_id', None)             
        if vacancy is not None:                                 
            return Application.objects.filter(vacancy=vacancy) 
        return Application.objects.all()   

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        vacancy = self.kwargs.get('vacancy_id', None)
        context['vacancy_id'] = Vacancy.objects.get(id=vacancy)
        
        # context['logo'] = Company.objects.get(vacancy=vacancy_id).logo
        return context