from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy, reverse

from django.views.generic import (
    UpdateView,
)

from .models import User

from forms import LoginForm, UserForm

class LogIn(FormView):
    template_name = 'users/login/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        return super(LogIn, self).form_valid(form)


class UserUpdateView(UpdateView):

    model = User
    form_class = UserForm
    template_name = 'users/usuario/update.html'
    success_url = reverse_lazy('profiles_app:dashboard')

    def form_valid(self, form):
        #recuperamos el usuario y guardamos
        usuario = self.get_object()
        usuario.set_password(form.cleaned_data['password1'])
        usuario.save()
        print '====guardado correctamente===='
        return super(UserUpdateView, self).form_valid(form)
