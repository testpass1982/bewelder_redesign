from django.shortcuts import render

# Create your views here.

def main(request):
    title = 'Bewelder learning project'
    return render(request, 'mainapp/index.html', context={'title': title})