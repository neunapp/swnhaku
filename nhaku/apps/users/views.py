from django.shortcuts import render
from django.views.generic import TemplateView


class LogIn(TemplateView):
    template_name='users/login/login.html'
