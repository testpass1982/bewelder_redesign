from django.urls import path

from search import forms
from haystack.views import SearchView

app_name = 'search'
urlpatterns = [
    path('', SearchView(form_class=forms.SearchForm), name='search'),
]