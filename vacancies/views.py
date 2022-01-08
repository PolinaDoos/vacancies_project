from django.contrib import messages
from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from vacancies.models import Application, Company, Specialty, Vacancy
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import ApplicationForm, CompanyForm, VacancyForm


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
        print(vacancy_data.id)
        skills = vacancy_data.skills.split(",")
        context = {
            'vacancy_data': vacancy_data,
            'skills': skills,
        }
        return render(request, 'vacancy_card.html', context)
    except Vacancy.DoesNotExist:
        return redirect(main_view)


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

# для работы с запросами в shell: 
# import django.contrib.auth.models as auth - auth.User.objects.all()
# import vacancies.models as models -> models.Company.objects.all()

@login_required
def mycompany(request):
    form = get_object_or_404(Company, owner=request.user)
    logo = form.logo
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=form)
        print(request.user.company)
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


def send_application(request, vacancy):
    if request.method == "POST":
        form= ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = Vacancy.objects.get(id=vacancy)
            application.user = request.user
            application.save()
            messages.success(request, 'Отклик отправлен')
            return redirect('vacancies')
        else:
            messages.error(request, 'Ошибка в заполнении формы')
    else:
        form = ApplicationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'vacancy', context)



class MySignupView(CreateView):
   form_class = UserCreationForm
   success_url = 'login'
   template_name = 'signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'