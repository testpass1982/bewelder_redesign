from django.urls import path

import vacancies.views as vacancies

app_name = 'vacancies'
urlpatterns = [
    path('list', vacancies.list, name='list'),
    # path('new', vacancies.new, name='new'),
    # path('edit', vacancies,edit, name='edit'),
]
