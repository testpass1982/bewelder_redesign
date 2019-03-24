from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse

from orgs.models import Employer, City
from orgs.forms import EmployerForm
from vacancies.models import Vacancy


EMPLOYERS_PER_PAGE = 5
VACANCIES_ON_SIDE_PANEL = 6
CITY_SEARCH_LIST_QUANTITY = 10


class EmployerListView(ListView):
    model = Employer
    template_name = 'orgs/employer_list.html'
    context_object_name = 'employers'
    paginate_by = EMPLOYERS_PER_PAGE


class EmployerDetailView(DetailView):
    model = Employer
    template_name = 'orgs/employer_detail.html'
    context_object_name = 'employer'


class EmployerCreateView(LoginRequiredMixin, CreateView):
    form_class = EmployerForm
    template_name = 'orgs/employer_form.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'employer') and user.employer.id:
            return redirect('orgs:update')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        employer = form.save(commit=False)
        employer.user = self.request.user
        employer.save()
        return redirect('orgs:detail', pk=employer.id)


class EmployerUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EmployerForm

    def get_object(self, queryset=None):
        return self.request.user.employer


class EmployerDeleteView(LoginRequiredMixin, DeleteView):
    model = Employer
    success_url = reverse_lazy('mainapp:settings')

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_anonymous or not (hasattr(user, 'employer') and bool(user.employer.id)):
            raise Http404
        return user.employer


# class CitySearchView(View):
#     def get(self, request):
#         if 'name' in self.kwargs:
#             cities = City.objects.filter(name__istartswith=self.kwargs['name']).order_by('name')
#         else:
#             cities = City.objects.filter().order_by('name')
#
#         data = {'cities': list(
#             cities.values(
#                 'id', 'name'
#             )[:CITY_SEARCH_LIST_QUANTITY])}
#
#         return JsonResponse(data)


def get_city_search_list(request, name=False):
    if name:
        cities = City.objects.filter(name__istartswith=name).order_by('name')
    else:
        cities = City.objects.filter().order_by('name')

    data = {'cities': list(
        cities.values(
            'id', 'name'
        )[:CITY_SEARCH_LIST_QUANTITY])}

    return JsonResponse(data)


def get_city_vacancies_list(request, city_id=False):
    if city_id:
        vacancies = Vacancy.objects.filter(employer__city=city_id).order_by('-id')
    else:
        vacancies = Vacancy.objects.all().order_by('-id')

    vacancies_list = []
    for vacancy in vacancies.values('id', 'created_date', 'title', 'employer__city__name', 'salary_min',
                                    'employer__short_name')[:VACANCIES_ON_SIDE_PANEL]:
        vacancy['created_date'] = vacancy['created_date'].strftime("%d %B %Y")
        vacancies_list.append(vacancy)

    data = {'vacancies': vacancies_list}

    return JsonResponse(data)
