from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from orgs.models import Employer
from orgs.forms import EmployerForm
from vacancies.models import Vacancy


EMPLOYERS_PER_PAGE = 5
VACANCIES_ON_SIDE_PANEL = 6


class EmployerListView(ListView):
    model = Employer
    template_name = 'orgs/employer_list.html'
    context_object_name = 'employers'
    paginate_by = EMPLOYERS_PER_PAGE

    @staticmethod
    def vacancies():
        return Vacancy.objects.all().order_by('-id')[:VACANCIES_ON_SIDE_PANEL]


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
