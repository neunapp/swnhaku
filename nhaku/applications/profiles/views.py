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

from .models import Client

from .forms import ClientForm, ClientUpdateForm

# Create your views here.

#mantenimiento para Clientes
class ClientRegister(FormView):
    '''
        vista para registrar clientes
    '''
    template_name = 'profiles/client/add.html'
    form_class = ClientForm
    success_url = reverse_lazy('profiles_app:cliente-list')

    def form_valid(self, form):
        #registramos usuario
        usuario = User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password2'],
            type_user='3',
        )
        usuario.save()
        #registramos el cliente
        cliente = form.save(commit=False)
        cliente.user = self.request.user
        cliente.user_created = self.request.user
        cliente.save()

        return super(ClientRegister, self).form_valid(form)


class ClientUpdateView(UpdateView):
    '''
        vista para actualizar datos de cliente
    '''
    model = Client
    template_name = 'profiles/client/update.html'
    form_class = ClientUpdateForm
    success_url = reverse_lazy('profiles_app:cliente-list')

    def form_valid(self, form):
        #recuperamos y actualizamos usuario de modificacion
        cliente = self.get_object()
        cliente.user_modified = self.request.user
        cliente.save()

        return super(ClientUpdateView, self).form_valid(form)


class ClientDetailView(DetailView):
    '''
        vista para mostra los datos de un cliente en detalle
    '''
    model = Client
    template_name = 'profiles/client/detail.html'


class ClientDeleteView(DetailView):
    '''
    Eliminar Client.
    '''
    model = Client
    template_name = 'profiles/client/delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # recuperamos el objeto y actualizamos a anulado
        cliente = self.object
        cliente.state = True
        cliente.save()
        return HttpResponseRedirect(
            reverse(
                'profiles_app:cliente-list'
            )
        )


class ClientListView(ListView):
    '''
        muestra la lista de clientes no eliminados
    '''
    context_object_name = 'client_list'
    template_name = 'profiles/client/list.html'
    paginate_by = 20

    def get_queryset(self):
        #recuperamos el valor por GET
        queryset = Client.objects.filter(state=False)
        return queryset


class Dashboard(TemplateView):
    template_name = 'profiles/cliente/add.html'
