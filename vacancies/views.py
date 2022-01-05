from django.contrib import messages
from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from vacancies.models import Company, Specialty, Vacancy
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CompanyForm, VacancyForm


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
        'user': request.user,
    }
    return render(request, 'index.html', context)


def vacancies(request):
    context = {
        'all_vacancies': Vacancy.objects.all(),
        'number_of_vacancies': len(Vacancy.objects.all())
    }
    return render(request, 'vacancies.html', context)


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
        # if Company.objects.all().values_list('company_original_id') and company in Company.objects.all().values_list('company_original_id', flat=True):
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


def vacancy(request, vacancy):
    try:
        vacancy_data = Vacancy.objects.get(id=vacancy)
        skills = vacancy_data.skills.split(", ")
        context = {
            'vacancy_data': vacancy_data,
            'skills': skills,
        }
        return render(request, 'vacancy_card.html', context)
    except Vacancy.DoesNotExist:
        return redirect(main_view)


def vacancy_send(request, vacancy):
    pass


@login_required
def start_company(request):
    messages.info(request, 'успех')
    return redirect(main_view)


@login_required
def create_company(request):
    form = CompanyForm()
    if request.method == "POST":
        form= CompanyForm(request.POST)
        messages.info(request, f'{request.user.username}, данные с формы получены')
        print(request.user.username)
        if form.is_valid():
            messages.info(request, 'форма валидна')
            Company.objects.create(owner=request.user, **form.cleaned_data)
            messages.success(request, 'успех')
            return redirect(main_view)
        else:
            messages.error(request, 'Ошибка в заполнении формы')
        
    context = {
        'form': form,
    }
    return render(request, 'create_company.html', context)


@login_required
def create_vacancy(request):
    form = VacancyForm()
    company = Company.objects.get(owner=request.user)
    published_at = datetime.today()
    if request.method == "POST":
        form= VacancyForm(request.POST)
        if form.is_valid():
            Vacancy.objects.create(company=company, published_at=published_at, **form.cleaned_data)
            messages.success(request, 'успех')
            return redirect(main_view)
        else:
            messages.error(request, 'Ошибка в заполнении формы')
        
    context = {
        'form': form,
        'company': company,
    }
    return render(request, 'create_vacancy.html', context)


class MySignupView(CreateView):
   form_class = UserCreationForm
   success_url = 'login'
   template_name = 'signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'