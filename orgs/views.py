from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from orgs.models import Employer
from orgs.forms import EmployerForm


EMPLOYERS_PER_PAGE = 5


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


# class EmployerUpdateView(LoginRequiredMixin, UpdateView):
#     form_class = EmployerForm
#     template_name = 'orgs/employer_form.html'
#
    # def get_object(self, queryset=None):
    #     return self.request.user.employer


class EmployerUpdateView:
    pass


class EmployerDeleteView:
    pass
