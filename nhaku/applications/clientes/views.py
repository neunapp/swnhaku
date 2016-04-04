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
    View,
)
from django.views.generic.edit import FormView

from .forms import SearchForm, FilterForm, PanelForm

from applications.recepcion.models import Guide, Manifest


class SearchView(ListView):
    '''
    vista para buscar una guia entregada
    '''
    context_object_name = 'list_guide'
    paginate_by = 20
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


class FilterView(ListView):
    '''
    vista para mostrar guias no entregdas
    '''
    context_object_name = 'list_guide'
    paginate_by = 20
    template_name = 'clientes/guias/filter.html'

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("tipo", '')
        queryset = Guide.objects.no_deliver(q)
        return queryset


class PanelView(ListView):
    '''
    vista para mostrra los manifiestos y guias de un cliente
    '''
    context_object_name = 'list_manifest'
    paginate_by = 20
    template_name = 'clientes/panel/index.html'

    def get_context_data(self, **kwargs):
        context = super(PanelView, self).get_context_data(**kwargs)
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


class GuideHistoryView(DetailView):
    '''
    vista para mostrar el historial de una guia
    '''
    model = Guide
    template_name = 'clientes/panel/history.html'
