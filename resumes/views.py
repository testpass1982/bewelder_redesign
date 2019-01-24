from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from resumes.forms import ResumeForm
from resumes.models import Resume


class ResumeList(ListView):
    model = Resume
    paginate_by = 10
    context_object_name = 'resumes'


class ResumeDetail(DetailView):
    model = Resume
    context_object_name = 'resume'


class ResumeCreate(LoginRequiredMixin, CreateView):
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'resume') and user.resume.id:
            return redirect('resumes:resume_update')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.user = self.request.user
        resume.save()
        return redirect('resumes:resume_detail', pk=resume.id)


class ResumeUpdate(LoginRequiredMixin, UpdateView):
    form_class = ResumeForm

    def get_object(self, queryset=None):
        return self.request.user.resume
