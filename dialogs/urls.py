from django.urls import path
from django.views.generic import TemplateView

app_name = 'dialogs'
urlpatterns = [
    path('messenger/', TemplateView.as_view(template_name='dialogs/messenger.html')),
]