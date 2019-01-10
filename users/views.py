from django.views import generic
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
from users.models import User


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
