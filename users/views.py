from django.views import generic

from users.forms import UserRegistrationForm
from users.models import User


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = '/'
    template_name = 'users/registration.html'
