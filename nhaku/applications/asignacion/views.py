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

from applications.users.models import User

from .models import Car

from .forms import CarForm

# Create your views here.

#mantenimiento para Vehiculo
class CarRegister(FormView):
    '''
        vista para registrar Vehiculos
    '''
    template_name = 'asignacion/car/add.html'
    form_class = CarForm
    success_url = reverse_lazy('asignacion_app:car-list')

    def form_valid(self, form):
        #registramos el cliente
        vehiculo = form.save(commit=False)
        vehiculo.user_created = self.request.user
        vehiculo.save()

        return super(CarRegister, self).form_valid(form)


class CarUpdateView(UpdateView):
    '''
        vista para actualizar datos de vehiculo
    '''
    model = Car
    template_name = 'asignacion/car/update.html'
    form_class = CarForm
    success_url = reverse_lazy('asignacion_app:car-list')

    def form_valid(self, form):
        #recuperamos y actualizamos usuario de modificacion
        form.save()
        vehiculo = self.get_object()
        vehiculo.user_modified = self.request.user
        vehiculo.save()

        return super(CarUpdateView, self).form_valid(form)


class CarDetailView(DetailView):
    '''
        vista para mostra los datos de un vehiculo en detalle
    '''
    model = Car
    template_name = 'asignacion/car/detail.html'


class CarDeleteView(DetailView):
    '''
    Eliminar Car.
    '''
    model = Car
    success_url = reverse_lazy('asignacion_app:car-list')
    template_name = 'asignacion/car/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        #desabilitamos Conductor
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class CarListView(ListView):
    '''
    muestra la lista de vehiculos no eliminados
    '''
    context_object_name = 'car_list'
    template_name = 'asignacion/car/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Car.objects.filter(state=False)
        return queryset
