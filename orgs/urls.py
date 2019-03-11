from django.urls import path

from orgs.views import EmployerListView, EmployerDetailView, EmployerCreateView,\
    EmployerUpdateView, EmployerDeleteView, get_city_search_list, get_city_vacancies_list

app_name = 'orgs'
urlpatterns = [
    path('', EmployerListView.as_view(), name='list'),
    path('<int:pk>/', EmployerDetailView.as_view(), name='detail'),
    path('create/', EmployerCreateView.as_view(), name='create'),
    path('update/', EmployerUpdateView.as_view(), name='update'),
    path('delete/', EmployerDeleteView.as_view(), name='delete'),
    path('city-search-list/<str:name>/', get_city_search_list, name='city_search_list'),
    path('city-search-list/', get_city_search_list, name='city_search_list'),
    # path('city-search-list/<str:name>/', CitySearchView.as_view(), name='city_search_list'),
    # path('city-search-list/', CitySearchView.as_view(), name='city_search_list'),
    path('city-vacancies-list/', get_city_vacancies_list, name='city_vacancies_list'),
    path('city-vacancies-list/<int:city_id>/', get_city_vacancies_list, name='city_vacancies_list'),
]
