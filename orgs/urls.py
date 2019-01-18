from django.urls import path

import orgs.views as orgs

app_name = 'orgs'
urlpatterns = [
    path('', orgs.EmployerListView.as_view(), name='list'),
]
