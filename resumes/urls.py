from django.urls import path

from resumes import views

app_name = 'resumes'
urlpatterns = [
    path('<int:pk>', views.ResumeDetail.as_view(), name='resume_detail'),
    path('', views.ResumeList.as_view(), name='resume_list'),

]
