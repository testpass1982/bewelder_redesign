from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from users.forms import UserRegistrationForm
from users.models import User


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'


@method_decorator(login_required, name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    template_name = 'users/profile_update.html'
    fields = 'first_name', 'last_name', 'email', 'date_of_birth'
    success_url = reverse_lazy('main')
    
    def get_object(self):
        return self.request.user
