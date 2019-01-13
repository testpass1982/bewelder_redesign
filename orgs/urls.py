from django.urls import path

import orgs.views as orgs

app_name = 'orgs'
urlpatterns = [
    path('list/', orgs.list, name='orgs_list'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('registration/', views.UserRegistrationView.as_view(), name='registration'),
]
