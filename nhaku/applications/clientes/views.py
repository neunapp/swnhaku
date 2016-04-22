# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    View,
)
from django.views.generic.edit import FormView

from .forms import SearchForm, PanelForm, ProfileForm

from .functions import report_guides, historia_guia

from applications.recepcion.models import Guide, Manifest, Observations
from applications.profiles.models import Client
from applications.asignacion.models import DetailAsignation
from applications.users.models import User


class SearchView(LoginRequiredMixin, ListView):
    '''
    vista para buscar una guia entregada
    '''
    context_object_name = 'list_guide'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'clientes/guias/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("number", '')
        queryset = Guide.objects.guide_deliver(q)
        return queryset


class PanelView(LoginRequiredMixin, ListView):
    '''
    vista para mostrra los manifiestos y guias de un cliente
    '''
    context_object_name = 'list_manifest'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'clientes/panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)
        queryset = kwargs.pop('object_list',self.object_list)
        context['reporte'] = report_guides(queryset)
        context['form'] = PanelForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("date", '')
        queryset = Manifest.objects.manifest_and_guide(
            self.request.user,
            q,
        )
        return queryset


class ProfileClient(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('users_app:login')
    template_name = 'clientes/panel/perfil.html'

    def form_valid(self, form):
        usuario = self.request.user
        cliente = Client.objects.get(
            user=usuario,
        )
        foto = form.cleaned_data['image']
        if foto:
            cliente.avatar = foto
            cliente.save()

        passwd = form.cleaned_data['password2']
        if len(passwd)>1:
            usuario.set_password(passwd)
            usuario.save()

        return super(ProfileClient, self).form_valid(form)


class GuideHistoryView(LoginRequiredMixin, DetailView):
    '''
    vista para mostrar el historial de una guia
    '''
    model = Guide
    login_url = reverse_lazy('users_app:login')
    template_name = 'clientes/panel/history.html'


    def get_context_data(self, **kwargs):
        context = super(GuideHistoryView, self).get_context_data(**kwargs)
        context['asignacion'] = DetailAsignation.objects.filter(
            guide=self.get_object(),
            guide__anulate=False,
        )
        context['list_obs'] = Observations.objects.filter(
            guide=self.get_object(),
            type_observation='0',
        ).order_by('created')
        context['historia'] = historia_guia(self.get_object())
        return context
