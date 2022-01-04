from django.db import models
from django.db.models.deletion import CASCADE, SET
from django.db.models.fields import CharField, DateField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


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


class Company(models.Model):
    name = CharField(max_length=200)
    location = CharField(max_length=200)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=60)
    width_field = models.PositiveIntegerField(default=100)
    description = TextField()
    employee_count = IntegerField()
    owner = OneToOneField('auth.User', on_delete=CASCADE, related_name='company', blank=True, null=True)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = CharField(max_length=200)
    title = CharField(max_length=200)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=80)
    width_field = models.PositiveIntegerField(default=80)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = CharField(max_length=200)
    written_phone = IntegerField()
    written_cover_letter = TextField(blank=True)
    vacancy = ForeignKey('Vacancy', on_delete=CASCADE, related_name="applications")
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name="applications")

    def __str__(self):
        return f'{self.written_username} vacancy {self.vacancy}'
