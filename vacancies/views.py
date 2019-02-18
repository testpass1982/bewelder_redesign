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
from django.shortcuts import get_object_or_404
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

def vacancy_details(request, pk):
    vacancy = Vacancy.objects.get(pk=pk)
    title = vacancy.title

    content = {
        'title': title,
        'vacancy': vacancy,
    }

    return render(request, 'vacancies/includes/vacancy_details.html', content)

@login_required
def add_new_vacancy(request):
    if request.user.is_authenticated:
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

@login_required
def vacancy_update(request, pk):
    if request.user.is_authenticated:
        instance = get_object_or_404(Vacancy, pk=pk, user=request.user)
        form = VacancyForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return HttpResponseRedirect(reverse('mainapp:settings'))
            else:
                print('ERRORS', form.errors.as_data())
        content = {
            'title': 'Обновление вакансии',
            'form': form,
        }
    return render(request, 'vacancies/update-vacancy.html', content)

@login_required
def vacancy_delete(request, pk):
    if request.user.is_authenticated:
        vacancy = get_object_or_404(Vacancy, pk=pk, user=request.user)
        if request.method == "POST":
            if 'Confirm' in request.POST:
                vacancy.delete()
                return HttpResponseRedirect(reverse('mainapp:settings'))
        content = {
            'vacancy': vacancy
        }

    return render(request, 'vacancies/vacancy_confirm_delete.html', content)



