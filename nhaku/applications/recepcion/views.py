# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
)
from django.views.generic.edit import FormView

from .forms import ManifestForm

from .models import Manifest

# Create your views here.

class ManifestCreateView(CreateView):
    model = Manifest
    form_class = ManifestForm
    success_url = '/'
    template_name = 'recepcion/manifest/add.html'

    def form_valid(self, form):
        manifiesto = form.save(commit=False)
        manifiesto.user = self.request.user
        manifiesto.user_created = self.request.user
        manifiesto.save()

        return super(ManifestCreateView, self).form_valid(form)
