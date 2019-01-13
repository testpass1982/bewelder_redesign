from django.shortcuts import render
from .models import Employer


def list(request):
    title = 'Список работодателей',

    employer_list = Employer.objects.all().order_by('short_name')

    content = {
        'title': title,
        'employer_list': employer_list
    }

    return render(request, 'orgs/list.html', content)
