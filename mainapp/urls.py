from django.urls import path

from mainapp import views


app_name = 'mainapp'
urlpatterns = [
    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    path('', views.HomePageView.as_view(), name='home'),
]