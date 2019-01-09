from django.urls import include, path

from . import views

app_name = 'users'
urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
]
