import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()


from vacancies.models import Company, Specialty, Vacancy
import mok_data


for i in mok_data.specialties:
    Specialty.objects.create(code=i.get('code'), title=i.get('title')).save()


for i in mok_data.companies:
    logo_file_path = f"/static/{i.get('logo')}"
    Company.objects.create(
        name = i.get('title'),
        location = i.get('location'),
        logo = logo_file_path,
        # company_original_id = i.get('id'),
        description = i.get('description'),
        employee_count = i.get('employee_count'),      
        ).save()


for i in mok_data.jobs:
    specialty = Specialty.objects.get(code=i.get('specialty'))
    # company = Company.objects.get(company_original_id=i.get('company'))
    company = Company.objects.get(id=i.get('company'))

    Vacancy.objects.create(
        title = i.get('title'),
        specialty = specialty,
        company = company,
        skills = i.get('skills'),
        description = i.get('description'),
        salary_min = i.get('salary_from'),
        salary_max = i.get('salary_to'),
        published_at =i.get('posted'),
        ).save()
