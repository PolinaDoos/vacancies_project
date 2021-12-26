from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from vacancies.models import Company, Specialty, Vacancy


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Или ничего нет. Простите, извините!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не отвечает именно Вам')


def main_view(request):
    specialty_vacancies = {}
    for i in Specialty.objects.all():
        specialty_vacancies[i.code] = len(Vacancy.objects.filter(specialty=i.id))

    company_vacancies = {}
    for i in Company.objects.all():
        company_vacancies[i.name] = len(Vacancy.objects.filter(company=i.id))

    context = {
        'all_companies': Company.objects.all(),
        'specialty_vacancies': specialty_vacancies,
        'company_vacancies': company_vacancies,
        'all_specialty': Specialty.objects.all()
    }
    return render(request, 'index.html', context)


def vacancies(request):
    all_vacancies = Vacancy.objects.all()
    context = {
        'all_vacancies': all_vacancies,
        'number_of_vacancies': len(all_vacancies)
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
        company_data = Company.objects.get(company_original_id=company)
        vacancies_data = Vacancy.objects.filter(company=company_data.id)
        print(vacancies_data)
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
        context = {
            'vacancy_data': vacancy_data,
        }
        return render(request, 'vacancy_card.html', context)
    except Vacancy.DoesNotExist:
        return redirect(main_view)
