from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from resumes.models import Resume


User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resumes = Resume.objects.all()
        context['resumes'] = resumes[:5]
        context['resumes_count'] = resumes.count()
        return context


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # something
        return context


# Create your views here.

# def main(request):
#     title = 'Bewelder learning project'
#     return render(request, 'mainapp/index.html', context={'title': title})
