# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
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

from .models import Client, Driver, Employee

from .forms import (
    ClientForm,
    ClientUpdateForm,
    DriverForm,
    DriverUpdateForm,
    EmployeeForm,
    EmployeeUpdateForm,
)

# Create your views here.

#mantenimiento para Clientes
class ClientRegister(LoginRequiredMixin, FormView):
    '''
        vista para registrar clientes
    '''
    template_name = 'profiles/client/add.html'
    form_class = ClientForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:cliente-list')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        # registramos usuario
        usuario = User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password2'],
            type_user='3',
        )
        usuario.save()
        #registramos el cliente
        cliente = form.save(commit=False)
        cliente.user = usuario
        cliente.user_created = self.request.user
        cliente.save()

        return super(ClientRegister, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    '''
        vista para actualizar datos de cliente
    '''
    model = Client
    template_name = 'profiles/client/update.html'
    form_class = ClientUpdateForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:cliente-list')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def form_valid(self, form):
        #recuperamos y actualizamos usuario de modificacion
        form.save()
        cliente = self.get_object()
        cliente.user_modified = self.request.user
        cliente.save()

        return super(ClientUpdateView, self).form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    '''
        vista para mostra los datos de un cliente en detalle
    '''
    model = Client
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/client/detail.html'

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Eliminar Cliente.
    '''
    model = Client
    template_name = 'profiles/client/delete.html'
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:cliente-list')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = self.object.user
        #Desactivamos usuario
        usuario.is_active = False
        usuario.save()
        #desabilitamos Conductor
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class ClientListView(LoginRequiredMixin, ListView):
    '''
    muestra la lista de clientes no eliminados
    '''
    context_object_name = 'client_list'
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/client/list.html'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            #recuperamos el valor por GET
            queryset = Client.objects.filter(state=False)
            return queryset


#mantenimientos para Conductor
class DriverListView(LoginRequiredMixin, ListView):
    '''
    metodo para listar conductores
    '''
    context_object_name = 'driver_list'
    model = Driver
    paginate_by = 10
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/driver/list.html'

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            queryset = Driver.objects.filter(state=False)
            return queryset


class DriverCreateView(LoginRequiredMixin, CreateView):
    '''
    metodo para registrar conductores
    '''
    model = Driver
    form_class = DriverForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:driver-list')
    template_name = 'profiles/driver/add.html'

    def get_context_data(self, **kwargs):
        context = super(DriverCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            return context

    def form_valid(self, form):
        #registramos usuario
        usuario = User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password1'],
            type_user='2',
        )
        usuario.save()
        #registramos conductor
        conductor = form.save(commit=False)
        conductor.user = usuario
        conductor.user_created = self.request.user
        conductor.save()

        return super(DriverCreateView, self).form_valid(form)


class DriverUpdateView(LoginRequiredMixin, UpdateView):
    '''
    vista para actualizar datos de conductor
    '''
    model = Driver
    template_name = 'profiles/driver/update.html'
    form_class = DriverUpdateForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:driver-list')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def form_valid(self, form):
        #recuperamos y actualizamos usuario de modificacion
        form.save()
        conductor = self.get_object()
        conductor.user_modified = self.request.user
        conductor.save()

        return super(DriverUpdateView, self).form_valid(form)


class DriverDetailView(LoginRequiredMixin, DetailView):
    '''
    vista para mostra los datos de un conductor en detalle
    '''
    model = Driver
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/driver/detail.html'

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    '''
    vista para desabilitar un conductor
    '''
    model = Driver
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:driver-list')
    template_name = 'profiles/driver/delete.html'

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = self.object.user
        #Desactivamos usuario
        usuario.is_active = False
        usuario.save()
        #desabilitamos Conductor
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


#mantenimietos para empleados
class EmployeeListView(LoginRequiredMixin, ListView):
    '''
    metodo para listar empleados
    '''
    context_object_name = 'employee_list'
    model = Employee
    paginate_by = 10
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/employee/list.html'

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            queryset = Employee.objects.filter(state=False)
            return queryset


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    '''
    metodo para registrar Empleados
    '''
    model = Employee
    form_class = EmployeeForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:employee-list')
    template_name = 'profiles/employee/add.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            return context

    def form_valid(self, form):
        #registramos usuario
        usuario = User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password1'],
            type_user='1',
        )
        usuario.save()
        #registramos empleado
        empleado = form.save(commit=False)
        empleado.user = usuario
        empleado.user_created = self.request.user
        empleado.save()

        return super(EmployeeCreateView, self).form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    '''
    vista para actualizar datos de Empleados
    '''
    model = Employee
    template_name = 'profiles/employee/update.html'
    form_class = EmployeeUpdateForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:employee-list')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def form_valid(self, form):
        #recuperamos y actualizamos usuario de modificacion
        form.save()
        conductor = self.get_object()
        conductor.user_modified = self.request.user
        conductor.save()
        return super(EmployeeUpdateView, self).form_valid(form)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    '''
    vista para mostra los datos de un Empleado en detalle
    '''
    model = Employee
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/employee/detail.html'

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    '''
    vista para desabilitar un Empleado
    '''
    model = Employee
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('profiles_app:employee-list')
    template_name = 'profiles/employee/delete.html'

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = self.object.user
        #Desactivamos usuario
        usuario.is_active = False
        usuario.save()
        #desabilitamos Empleado
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


# class Dashboard(TemplateView):
#     template_name = 'users/cliente/detail_guia.html'


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users_app:login')
    template_name = 'profiles/panel/dashboard.html'
