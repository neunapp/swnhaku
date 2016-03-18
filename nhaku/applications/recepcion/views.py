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

from .models import Manifest, Guide

# Create your views here.

class ManifestCreateView(CreateView):
    '''
    vista para crear un manifiesto
    '''
    model = Manifest
    form_class = ManifestForm
    success_url = reverse_lazy('recepcion_app:manifest-list')
    template_name = 'recepcion/manifest/add.html'

    def form_valid(self, form):
        manifiesto = form.save(commit=False)
        manifiesto.user_created = self.request.user
        manifiesto.save()

        return super(ManifestCreateView, self).form_valid(form)


class ManifestUpdateView(UpdateView):
    '''
    vista para actualizar un manifiesto
    '''
    model = Manifest
    template_name = 'recepcion/manifest/update.html'
    form_class = ManifestForm
    success_url = reverse_lazy('recepcion_app:manifest-list')

    def get_context_data(self, **kwargs):
        context = super(ManifestUpdateView, self).get_context_data(**kwargs)
        manifiesto = self.get_object()
        #listamos las guis de este manifiesto
        context['list_guias'] = Guide.objects.by_manifest(manifiesto)
        return context

    def form_valid(self, form):
        #recuperamos y duardamos el manifiesto
        manifiesto = self.get_object()
        manifiesto.user_modified = self.request.user
        manifiesto.save()

        return super(ManifestUpdateView, self).form_valid(form)

class ManifestDetailView(DetailView):
    '''
    vista para ver el detalle y lista de guas de una mnifiesto
    '''
    model = Manifest
    template_name = 'recepcion/manifest/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ManifestDetailView, self).get_context_data(**kwargs)
        manifiesto = self.get_object()
        #listamos las guis de este manifiesto
        context['list_guias'] = Guide.objects.by_manifest(manifiesto)
        return context


class ManifestDeleteView(DeleteView):
    '''
    metodo para eliminar o poner manifiesto en eliminado
    '''
    model = Manifest
    template_name = 'recepcion/manifest/delete.html'
    success_url = reverse_lazy('recepcion_app:manifest-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.state = True
        self.object.user_modified = self.request.user
        #eliminamos las guis del manifiesto
        Guide.objects.delete_guides(self.object, self.request.user)
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class ManifestListView(ListView):
    '''
        muestra la lista de manifiestos
    '''
    context_object_name = 'manifest_list'
    template_name = 'recepcion/manifest/list.html'
    paginate_by = 20

    def get_queryset(self):
        #recuperamos el valor por GET
        queryset = Manifest.objects.filter(state=False)
        return queryset
