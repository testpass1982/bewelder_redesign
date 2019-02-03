from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from orgs.models import Employer
from .models import Vacancy, Level
from .forms import VacancyForm
# from orgs.forms import EmployerForm, RegionForm, CityForm
from django.contrib.auth.decorators import login_required
# from django.forms.formsets import formset_factory
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

@login_required
def add_new_vacancy(request):
    title = 'Добавление вакансии'
    # TODO: need to make a form to choice or add employer with region and city
    if request.method == 'POST':
        form = VacancyForm(request.POST)

        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('mainapp:settings'))
    else:
        form = VacancyForm()

    content = {
        'title' : title,
        'form': form,
    }
    return render(request, 'vacancies/add-new-vacancy.html', content)

def update_vacancy(request, pk):
    pass

def delete_vacancy(request, pk):
    pass



