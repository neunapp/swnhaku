# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
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

from .forms import ObservationsForm, DeliverForm

from applications.asignacion.models import Asignation, DetailAsignation
from applications.recepcion.models import Guide, Observations
from applications.clientes.forms import SearchForm


class ReceptionAsignationView(DetailView):
    '''
    clase para confirmar la recepcion de un vehiculo que volvio
    '''
    model = Asignation
    template_name = 'entrega/asignation/reception.html'

    def post(self, request, *args, **kwargs):
        #recuperamos la asignacion y actualizmos estado
        self.object = self.get_object()
        self.object.state = '2'
        self.object.save()
        #recuperamos la lista de guias y actualizamos estado
        guides = DetailAsignation.objects.filter(
            asignation=self.object,
        )
        for g in guides:
            if g.guide.state == '4':
                g.state = True
                g.save()
            else:
                g.state = False
                g.save()
                g.guide.state = '1'
                g.guide.priority = '0'
                g.guide.save()

        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list'
            )
        )


#Registrar observacin para guia en recepcion
class ObservationCreateView(CreateView):
    '''
    vista para gregar una nueva observacion a una una guia
    '''
    model = Observations
    form_class = ObservationsForm
    template_name = 'entrega/observations/add.html'

    def get_context_data(self, **kwargs):
        context = super(ObservationCreateView, self).get_context_data(**kwargs)
        context['asignation'] = self.kwargs.get('as', 0)
        return context

    def form_valid(self, form):
        obs = form.save(commit=False)
        #recuperamos la guia
        guide_pk = self.kwargs.get('pk', 0)
        guia = Guide.objects.get(pk=guide_pk)
        obs.guide = guia
        obs.user_created = self.request.user
        obs.save()
        asig = self.kwargs.get('as', 0)
        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list_guide',
                kwargs={'pk': asig },
            )
        )


class AsignationListView(ListView):
    '''
    vista para listar Asignaciones con estado en vehiculo o salio
    '''
    context_object_name = 'asignation_list'
    model = Asignation
    template_name = 'entrega/asignation/list.html'

    def get_queryset(self):
        queryset = Asignation.objects.filter(
            anulate=False,
            state='1',
        )
        return queryset


class GuideByAsignation(ListView):
    '''
    muestra la lista de guias de un Asignacion en entrega
    '''
    context_object_name = 'list_guides'
    paginate_by = 20
    template_name = 'entrega/asignation/list_guide.html'

    def get_context_data(self, **kwargs):
        context = super(GuideByAsignation, self).get_context_data(**kwargs)
        asignation_pk = self.kwargs.get('pk', 0)
        context['asignation'] = Asignation.objects.get(pk=asignation_pk)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        asignation_pk = self.kwargs.get('pk', 0)
        q = self.request.GET.get("number", '')
        queryset = DetailAsignation.objects.guide_by_asignation(
            asignation_pk,
            q
        )
        return queryset


class DeliverView(FormView):
    form_class = DeliverForm
    template_name = 'entrega/entrega/deliver.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverView, self).get_context_data(**kwargs)
        context['asignation'] = self.kwargs.get('as', 0)
        return context

    def form_valid(self, form):
        #recuperamos la guia
        guia = Guide.objects.get(pk=self.kwargs.get('pk', 0))
        guia.person_id = form.cleaned_data['dni']
        guia.person_name = form.cleaned_data['full_name']
        guia.date_deliver = datetime.now()
        guia.state = '4'
        guia.save()
        asig = self.kwargs.get('as', 0)
        return HttpResponseRedirect(
            reverse(
                'entrega_app:entrega-list_guides',
                kwargs={'pk': asig },
            )
        )


class DeliverObservation(CreateView):
    '''
    vista para gregar una nueva observacion a una una guia
    '''
    model = Observations
    form_class = ObservationsForm
    template_name = 'entrega/observations/add_deliver.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverObservation, self).get_context_data(**kwargs)
        context['asignation'] = self.kwargs.get('as', 0)
        return context

    def form_valid(self, form):
        obs = form.save(commit=False)
        #recuperamos la guia
        guide_pk = self.kwargs.get('pk', 0)
        guia = Guide.objects.get(pk=guide_pk)
        obs.guide = guia
        obs.user_created = self.request.user
        obs.save()
        asig = self.kwargs.get('as', 0)
        return HttpResponseRedirect(
            reverse(
                'entrega_app:entrega-list_guides',
                kwargs={'pk': asig },
            )
        )
