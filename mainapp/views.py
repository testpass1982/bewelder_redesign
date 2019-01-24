from django.shortcuts import render
from django.views.generic import TemplateView

from resumes.models import Resume



class HomePageView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Resume.objects.all()[:5]
        return context


# Create your views here.

# def main(request):
#     title = 'Bewelder learning project'
#     return render(request, 'mainapp/index.html', context={'title': title})