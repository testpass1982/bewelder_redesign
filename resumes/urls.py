from django.urls import path

from resumes import views

app_name = 'resumes'
urlpatterns = [
    path('<int:pk>', views.ResumeDetail.as_view(), name='resume_detail'),
    path('create/', views.ResumeCreate.as_view(), name='resume_create'),
    path('update/', views.ResumeUpdate.as_view(), name='resume_update'),
    path('delete/', views.ResumeDelete.as_view(), name='resume_delete'),
    path('', views.ResumeList.as_view(), name='resume_list'),

]
