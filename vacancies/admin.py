from django.contrib import admin

# Register your models here.
from .models import Company, Specialty, Vacancy


admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialty)