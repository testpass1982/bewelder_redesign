from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from orgs.models import Employer
from .models import Vacancy, Level
from .forms import VacancyForm, VacancySearchForm
# from orgs.forms import EmployerForm, RegionForm, CityForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from functools import reduce
import operator
# from django.forms.formsets import formset_factory
# Create your views here.

def vacancies_list(request):
    title = 'Список вакансий'
    if request.method == 'POST':
        vacancy_search_form = VacancySearchForm(request.POST)
        if vacancy_search_form.is_valid():
            request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
            print('REQUEST DICT', request_to_dict)
            #начинаем конфигурировать запрос к БД с помощью объекта Q
            query_list = [
                Q(business_trips='business_trips' in request_to_dict),
                Q(shift_work='shifted_work' in request_to_dict),
            ]
            #сопоставляем данные из POST с уровнями
            att_levels = {
                'naks_att_level1' : 'I',
                'naks_att_level2' : 'II',
                'naks_att_level3': 'III',
                'naks_att_level4': 'IV',
            }
            #собираем все уровни в список (для выбора из БД)
            att_levels_query = []
            for i in att_levels.keys():
                if i in request_to_dict.keys():
                    att_levels_query.append(att_levels[i])
            #print('LEVEL QUERY' , att_levels_query)
            #дополняем запрос  к БД в случае если выбран хотя бы один уровень
            if len(att_levels_query)!=0:
                levels_query = Q(naks_att_level__name__in=att_levels_query)
                query_list.append(levels_query)
            #Если в POST содержатся непустые поля по зарплате, добавляем их в список запросов
            if request_to_dict['salary_min'] !='':
                query_list.append(Q(salary_min__gte=request_to_dict['salary_min']))
            if request_to_dict['salary_max'] !='':
                query_list.append(Q(salary_max__lte=request_to_dict['salary_max']))
            #print('QUERY_LIST', query_list)
            #собираем запрос и выполняем последовательное
            #применение оператора И к каждому запросу в query list
            query = reduce(operator.and_, query_list)
            #print('QUERY', query)
            #формируем список вакансий
            filtered_vacancies=Vacancy.objects.filter(query)
            #print('RAW SQL', filtered_vacancies.query)
            context = {
                'title': 'Результаты поиска',
                'vacancies': filtered_vacancies,
                'vacancy_search_form': VacancySearchForm(initial=request_to_dict)
            }
            return render(request, 'vacancies/list.html', context)
    else:
        vacancy_search_form = VacancySearchForm()
    vacancy_list = Vacancy.objects.filter(
        published=True).order_by('created_date')
    paginator = Paginator(vacancy_list, 5)
    page = request.GET.get('page')
    vacancies = paginator.get_page(page)
    content = {
        'title': title,
        'vacancies': vacancies,
        'vacancy_search_form': vacancy_search_form,
    }
    return render(request, 'vacancies/list.html', content)

def vacancy_details(request, pk):
    vacancy = Vacancy.objects.get(pk=pk)
    related_vacancies = Vacancy.objects.all().exclude(pk=vacancy.pk)[:3]
    title = vacancy.title

    content = {
        'title': title,
        'vacancy': vacancy,
        'related_vacancies': related_vacancies,
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



