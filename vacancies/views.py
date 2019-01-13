from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Vacancy, Level
# Create your views here.

def list(request):
    title = 'Список вакансий'
    
    vacancy_list = Vacancy.objects.filter(
        published=True).order_by('created_date')
    paginator = Paginator(vacancy_list, 5)
    page = request.GET.get('page')
    vacancies = paginator.get_page(page)
    content = {
        'title': title,
        'vacancies': vacancies
    }
    return render(request, 'vacancies/list.html', content)


