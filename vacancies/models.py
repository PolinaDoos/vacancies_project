from django.db import models
from django.db.models.deletion import CASCADE, SET
from django.db.models.fields import CharField, DateField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey


class Vacancy(models.Model):
    title = CharField(max_length=200)
    specialty = ForeignKey('Specialty', on_delete=SET('IT'), related_name="vacancies")
    company = ForeignKey('Company', on_delete=CASCADE, related_name="companies")
    skills = TextField()
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateField()

    def __str__(self):
        return self.title


class Company (models.Model):
    name = CharField(max_length=200)
    company_original_id = IntegerField(null=True)
    location = CharField(max_length=200)
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()

    def __str__(self):
        return self.name


class Specialty (models.Model):
    code = CharField(max_length=200)
    title = CharField(max_length=200)
    picture = URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return self.title
