from django.views.generic import ListView, DetailView

from resumes.models import Resume


class ResumeList(ListView):
    model = Resume
    paginate_by = 10
    context_object_name = 'resumes'


class ResumeDetail(DetailView):
    model = Resume
    context_object_name = 'resume'
