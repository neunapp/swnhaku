from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from forms import LoginForm

class LogIn(FormView):
    template_name = 'users/login/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        return super(LogIn, self).form_valid(form)
