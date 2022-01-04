from django.contrib import admin

# Register your models here.
from .models import Application, Company, Specialty, Vacancy


admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Application)


# class UserAdmin(admin.ModelAdmin):

#     readonly_fields = ('show_companies',)

#     def show_companies(self, obj):
#         pass