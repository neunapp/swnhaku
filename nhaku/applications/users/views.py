from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy

# Autentificacion de usuario
from django.contrib.auth import authenticate, login, logout

from .models import User
from .forms import LoginForm, UserForm


class LogIn(FormView):
    '''
    Logeo del usuario
    '''
    template_name = 'users/login/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        # Verfiamos si el usuario y contrasenha son correctos.
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            if user.is_active:
                # si el usuario es activo ira dahboard
                login(self.request, user)
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
