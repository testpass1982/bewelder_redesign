from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from orgs.models import Employer
from .models import Vacancy, Level
from .forms import VacancyForm
# Create your views here.

def vacancies_list(request):
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

def add_new_vacancy(request):
    title = 'Добавление вакансии'
    if request.method == 'POST':
        # print(request.POST)
        form = VacancyForm(request.POST)

        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.user = request.user
            vacancy.employer = Employer.objects.get(pk=1)
            form.save()
            return HttpResponseRedirect(reverse('mainapp:settings'))
    else:
        form = VacancyForm()

    content = {
        'title' : title,
        'form': form,
    }
    return render(request, 'vacancies/add-new-vacancy.html', content)

def update_vacancy(request):
    pass

def delete_vacancy(request):
    pass



