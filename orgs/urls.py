from django.urls import path

from orgs.views import EmployerListView, EmployerDetailView, EmployerCreateView,\
    EmployerUpdateView, EmployerDeleteView

app_name = 'orgs'
urlpatterns = [
    path('', EmployerListView.as_view(), name='list'),
    path('<int:pk>/', EmployerDetailView.as_view(), name='detail'),
    path('create/', EmployerCreateView.as_view(), name='create'),
    path('update/<int:pk>/', EmployerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', EmployerDeleteView.as_view(), name='delete'),
]