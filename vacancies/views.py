from django.shortcuts import render
from .models import Vacancy, Level
# Create your views here.

def list(request):
    title = 'Список вакансий'

    vacancy_list = Vacancy.objects.filter(
        published=True).order_by('created_date')

    content = {
        'title': title,
        'vacancies': vacancy_list
    }
    return render(request, 'vacancies/list.html', content)


