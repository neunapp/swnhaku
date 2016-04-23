# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
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


class ReceptionAsignationView(LoginRequiredMixin, DetailView):
    '''
    clase para confirmar la recepcion de un vehiculo que volvio
    '''
    model = Asignation
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/asignation/reception.html'

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

    def post(self, request, *args, **kwargs):
        #recuperamos la asignacion y actualizmos estado
        self.object = self.get_object()
        self.object.state = '2'
        self.object.date_retunr = timezone.now()
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
class ObservationCreateView(LoginRequiredMixin, CreateView):
    '''
    vista para gregar una nueva observacion a una una guia
    '''
    model = Observations
    form_class = ObservationsForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/observations/add.html'

    def get_context_data(self, **kwargs):
        context = super(ObservationCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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


class AsignationListView(LoginRequiredMixin, ListView):
    '''
    vista para listar Asignaciones con estado en vehiculo o salio
    '''
    context_object_name = 'asignation_list'
    model = Asignation
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/asignation/list.html'

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            queryset = Asignation.objects.filter(
                anulate=False,
                state='1',
            )
            return queryset


class GuideByAsignation(LoginRequiredMixin, ListView):
    '''
    muestra la lista de guias de un Asignacion en entrega
    '''
    context_object_name = 'list_guides'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/asignation/list_guide.html'

    def get_context_data(self, **kwargs):
        context = super(GuideByAsignation, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
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


class DeliverView(LoginRequiredMixin, FormView):
    '''
    vista para registrar los datos de receptor de guia
    '''
    form_class = DeliverForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/entrega/deliver.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
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


class DeliverObservation(LoginRequiredMixin, CreateView):
    '''
    vista para gregar una nueva observacion a una una guia
    '''
    model = Observations
    form_class = ObservationsForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/observations/add_deliver.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverObservation, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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


class ListDeliverOffice(LoginRequiredMixin, ListView):
    '''
    muestra la lista de guias con entrega en oficina
    '''
    context_object_name = 'list_guides'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/entrega/office.html'

    def get_context_data(self, **kwargs):
        context = super(ListDeliverOffice, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            context['form'] = SearchForm
            return context

    def get_queryset(self):
        q = self.request.GET.get("number", '')
        queryset = Guide.objects.filter(
            number__icontains=q,
            anulate=False,
            state='1',
            type_guide='0',
        )
        return queryset


class DeliverOffice(LoginRequiredMixin, FormView):
    '''
    vista para registrar entrega guia en oficina
    '''
    form_class = DeliverForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'entrega/entrega/deliver_office.html'

    def get_context_data(self, **kwargs):
        context = super(DeliverOffice, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            context['guia'] = Guide.objects.get(pk=self.kwargs.get('pk', 0))
            return context

    def form_valid(self, form):
        #recuperamos la guia
        guia = Guide.objects.get(pk=self.kwargs.get('pk', 0))
        guia.person_id = form.cleaned_data['dni']
        guia.person_name = form.cleaned_data['full_name']
        guia.date_deliver = datetime.now()
        guia.state = '4'
        guia.save()
        return HttpResponseRedirect(
            reverse(
                'entrega_app:entrega-oficina',
            )
        )
