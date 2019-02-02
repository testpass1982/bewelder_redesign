from django.urls import path

import vacancies.views as vacancies

app_name = 'vacancies'
urlpatterns = [
    path('list/', vacancies.vacancies_list, name='list'),
    path('new/', vacancies.add_new_vacancy, name='vacancy_create'),
    # path('edit', vacancies,edit, name='edit'),
]
