from django.views import generic
from orgs.models import Employer


EMPLOYERS_PER_PAGE = 5


class EmployerListView(generic.ListView):
    model = Employer
    template_name = 'orgs/list.html'
    context_object_name = 'employer_list'
    paginate_by = EMPLOYERS_PER_PAGE
