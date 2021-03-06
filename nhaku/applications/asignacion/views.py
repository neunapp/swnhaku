# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    View,
)

from applications.users.models import User
from applications.recepcion.models import Guide

from .functions import generar_pdf

from .models import Car, Asignation, DetailAsignation

from .forms import CarForm, AsignationForm, AddAsignationForm

# Create your views here.

#mantenimiento para Vehiculo
class CarRegister(LoginRequiredMixin, FormView):
    '''
        vista para registrar Vehiculos
    '''
    template_name = 'asignacion/car/add.html'
    form_class = CarForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('asignacion_app:car-list')

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
        #registramos el cliente
        vehiculo = form.save(commit=False)
        vehiculo.user_created = self.request.user
        vehiculo.save()

        return super(CarRegister, self).form_valid(form)


class CarUpdateView(LoginRequiredMixin, UpdateView):
    '''
        vista para actualizar datos de vehiculo
    '''
    model = Car
    template_name = 'asignacion/car/update.html'
    form_class = CarForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('asignacion_app:car-list')

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
        vehiculo = self.get_object()
        vehiculo.user_modified = self.request.user
        vehiculo.save()

        return super(CarUpdateView, self).form_valid(form)


class CarDetailView(LoginRequiredMixin, DetailView):
    '''
        vista para mostra los datos de un vehiculo en detalle
    '''
    model = Car
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/car/detail.html'

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


class CarDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Eliminar Car.
    '''
    model = Car
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('asignacion_app:car-list')
    template_name = 'asignacion/car/delete.html'

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
        #desabilitamos Conductor
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class CarListView(LoginRequiredMixin, ListView):
    '''
    muestra la lista de vehiculos no eliminados
    '''
    context_object_name = 'car_list'
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/car/list.html'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            queryset = Car.objects.filter(state=False)
            return queryset


#mantenimientos para Asignaciones
class AsignationListView(LoginRequiredMixin, ListView):
    '''
    vista para listar Asignaciones no completadas
    '''
    context_object_name = 'asignation_list'
    model = Asignation
    paginate_by = 5
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/asignation/list.html'

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            queryset = Asignation.objects.filter(anulate=False).exclude(state='2')
            return queryset


class AsignationCreateView(LoginRequiredMixin, CreateView):
    '''
    vista para agregar una nueva asigancion
    '''
    model = Asignation
    form_class = AsignationForm
    login_url = reverse_lazy('users_app:login')
    success_url = success_url = reverse_lazy('asignacion_app:asignation-list')
    template_name = 'asignacion/asignation/add.html'

    def get_context_data(self, **kwargs):
        context = super(AsignationCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            return context

    def form_valid(self, form):
        #registramos el usuario de creacion y estado de la asigancion
        asignacion = form.save(commit=False)
        asignacion.state = '0'
        asignacion.user_created = self.request.user
        asignacion.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:zone-by_guide',
                kwargs={'pk': asignacion.pk },
            )
        )

        return super(AsignationCreateView, self).form_valid(form)


class AsignationDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Eliminar una Asignation.
    '''
    model = Asignation
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('asignacion_app:asignation-list')
    template_name = 'asignacion/asignation/delete.html'

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
        #desabilitamos la asignacion
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        #actualizamos el estado de las guias
        DetailAsignation.objects.guide_in_office(self.object)
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class AddGuideAsignationView(LoginRequiredMixin, FormView):
    '''
    vista para añadir guias a una asignacion
    '''
    template_name = 'asignacion/asignar/add_guide.html'
    login_url = reverse_lazy('users_app:login')
    form_class = AddAsignationForm

    def get_context_data(self, **kwargs):
        context = super(AddGuideAsignationView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            asignation_pk = self.kwargs.get('as', 0)
            context['asignation'] = Asignation.objects.get(pk=asignation_pk)
            return context

    def get_form_kwargs(self):
        kwargs = super(AddGuideAsignationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs.get('pk', 0),
        })
        return kwargs

    def form_valid(self, form):
        guias = form.cleaned_data['guide']
        #recuperamos la asignacion
        asignation_pk = self.kwargs.get('as', 0)
        asignation = Asignation.objects.get(pk=asignation_pk)
        for guia in guias:
            detail_asignation = DetailAsignation(
                asignation=asignation,
                guide=guia,
            )
            detail_asignation.save()
            guia.state = '2'
            guia.save()

        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list_guide',
                kwargs={'pk': asignation.pk },
            )
        )


class GuideByAsignationListView(LoginRequiredMixin, ListView):
    '''
    muestra la lista de guias de un Asignacion
    '''
    context_object_name = 'list_guides'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/asignar/list.html'

    def get_context_data(self, **kwargs):
        context = super(GuideByAsignationListView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            asignation_pk = self.kwargs.get('pk', 0)
            context['asignation'] = Asignation.objects.get(pk=asignation_pk)
            A,B = DetailAsignation.objects.weigth_by_asignation(
                Asignation.objects.get(pk=asignation_pk),
            )
            context['peso'] = A
            return context

    def get_queryset(self):
        asignation_pk = self.kwargs.get('pk', 0)
        queryset = DetailAsignation.objects.filter(
            asignation__pk=asignation_pk,
            guide__anulate=False,
        )
        return queryset


class ConfirmarAsignationView(LoginRequiredMixin, DetailView):
    '''
    vista para confrimar el despacho de una asignacion
    '''
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/asignar/confirmar.html'
    model = Asignation

    def get_context_data(self, **kwargs):
        context = super(ConfirmarAsignationView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #recuperamos el objeto y actualizamos a anulado
        self.object.state = '1'
        #actualizamos y guardamos el valor
        self.object.save()
        #recuperamos las guis de esta asignacion
        guias = DetailAsignation.objects.filter(
            asignation=self.object,
            guide__anulate=False,
        )
        #Actualizamos el estado de las guias a vehiculo
        for g in guias:
            g.guide.state = '3'
            g.guide.save()

        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list'
            )
        )


class DeleteAsignationDeleteView(LoginRequiredMixin, DetailView):
    '''
    Eliminar una asignacion detalle
    '''
    model = Asignation
    login_url = reverse_lazy('users_app:login')
    template_name = 'asignacion/asignar/delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteAsignationDeleteView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            context['guide'] = self.kwargs.get('guide', 0)
            return context

    def post(self, request, *args, **kwargs):
        #recuperamos la asignacion
        self.object = self.get_object()
        #recuperamos la guia
        guide_pk = self.kwargs.get('guide', 0)
        #recuperamos la guia
        guide = Guide.objects.get(pk=guide_pk)
        guide.state = '1'
        guide.save()
        #recuperamos la DetailAsignation
        detail_asignation = DetailAsignation.objects.get(
            asignation=self.object,
            guide=guide,
        )
        detail_asignation.delete()

        return HttpResponseRedirect(
            reverse(
                'asignacion_app:asignation-list_guide',
                kwargs={'pk': self.object.pk },
            )
        )


class ReportAsigView(LoginRequiredMixin, SingleObjectMixin, View):
    '''
    vista que imprime un pdf de la lista de guias de una asignacion
    '''

    model = Asignation
    login_url = reverse_lazy('users_app:login')

    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            return HttpResponseRedirect(
                reverse(
                    'users_app:login'
                )
            )
        else:
            asig = self.get_object()
            guides = DetailAsignation.objects.filter(
                asignation=asig,
            )
            return generar_pdf(
                'asignacion/report/print_asig.html',
                {'pagesize' : 'A4', 'guides' : guides, 'objeto':asig}
            )
