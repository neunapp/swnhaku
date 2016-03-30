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

from .forms import ObservationsForm

from applications.asignacion.models import Asignation, DetailAsignation
from applications.recepcion.models import Guide, Observations


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
                g.guide.save()

        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list'
            )
        )


#mantenimiento para observaciones
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
