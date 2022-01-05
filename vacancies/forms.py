from django import forms
from django.forms import ModelForm

from vacancies.models import Company, Vacancy


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count')


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')

