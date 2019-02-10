from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from orgs.models import Employer


EMPLOYERS_PER_PAGE = 5


class EmployerListView(ListView):
    model = Employer
    template_name = 'orgs/orgs_list.html'
    context_object_name = 'employer_list'
    paginate_by = EMPLOYERS_PER_PAGE


class EmployerDetailView(DetailView):
    model = Employer
    template_name = 'orgs/orgs_detail.html'
    context_object_name = 'employer'


class EmployerCreateView:
    pass


class EmployerUpdateView:
    pass


class EmployerDeleteView:
    pass

