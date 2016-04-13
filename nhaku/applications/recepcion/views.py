# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
    TemplateView,
    View,
)

from django.views.generic.edit import FormView

from .forms import (
    ManifestForm,
    GuideForm,
    ZoneForm,
    ReceptionForm,
    GuideUpdateForm,
    FilterForm,
)

from applications.entrega.forms import ObservationsForm

from applications.clientes.forms import SearchForm

from .models import Manifest, Guide, Zone, Observations

from applications.asignacion.models import Asignation
from applications.asignacion.functions import generar_pdf

from datetime import datetime

# Create your views here.

class ZoneCreateView(CreateView):
    '''
    vista para registrar zona nueva
    '''
    model = Zone
    form_class = ZoneForm
    success_url = reverse_lazy('recepcion_app:zone-list')
    template_name = 'recepcion/zone/add.html'

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.user_created = self.request.user
        zona.save()

        return super(ZoneCreateView, self).form_valid(form)


class ZoneUpdateView(UpdateView):
    '''
    vista para modificar una zona
    '''
    model = Zone
    template_name = 'recepcion/zone/update.html'
    form_class = ZoneForm
    success_url = reverse_lazy('recepcion_app:zone-list')

    def form_valid(self, form):
        form.save()
        zona = self.get_object()
        zona.user_modified = self.request.user
        zona.save()

        return super(ZoneUpdateView, self).form_valid(form)


class ZoneDeleteView(DeleteView):
    '''
    vista para desabilitar una zona
    '''
    model = Zone
    success_url = reverse_lazy('recepcion_app:zone-list')
    template_name = 'recepcion/zone/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class ZoneListView(ListView):
    '''
        muestra la lista de zonas
    '''
    context_object_name = 'zone_list'
    template_name = 'recepcion/zone/list.html'
    paginate_by = 10

    def get_queryset(self):
        #recuperamos el valor por GET
        queryset = Zone.objects.filter(state=False)
        return queryset


class Zone_by_GuideListView(ListView):
    '''
    lista de zonas que corresponden a guias en oficina
    '''
    context_object_name = 'zone_list'
    template_name = 'recepcion/zone/by_guides.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(Zone_by_GuideListView, self).get_context_data(**kwargs)
        asignation_pk = self.kwargs.get('pk', 0)
        context['asignacion'] = Asignation.objects.get(pk=asignation_pk)
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        queryset = Guide.objects.zones_by_guide()
        return queryset


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
        manifiesto.date = timezone.now()
        manifiesto.user_created = self.request.user
        manifiesto.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:guide-add',
                kwargs={'pk': manifiesto.pk },
            )
        )

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
        form.save()
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
        queryset = Manifest.objects.manifest_by_day()
        return queryset


class GuideCreateView(SuccessMessageMixin, CreateView):
    '''
    vista para registrar las guias de remision
    '''
    model = Guide
    form_class = GuideForm
    success_url = '.'
    template_name = 'recepcion/guide/add.html'
    success_message = "La Guia Se Guardo Correctamente..."

    def get_context_data(self, **kwargs):
        context = super(GuideCreateView, self).get_context_data(**kwargs)
        manifiesto_pk = self.kwargs.get('pk', 0)
        context['manifiesto'] = Manifest.objects.get(pk=manifiesto_pk)
        return context

    def form_valid(self, form):
        #guardamos la guia
        guia = form.save(commit=False)
        manifiesto_pk = self.kwargs.get('pk', 0)
        manifiesto = Manifest.objects.get(pk=manifiesto_pk)
        guia.manifest = manifiesto
        guia.state = '0'
        guia.user_created = self.request.user
        return super(GuideCreateView, self).form_valid(form)


class GuideUpdateView(UpdateView):
    '''
    metodo para modificar y actualizar una guia
    '''
    model = Guide
    template_name = 'recepcion/guide/update.html'
    form_class = GuideUpdateForm
    success_url = '.'

    def form_valid(self, form):
        #guardamos la guia
        form.save()
        guia = self.get_object()
        guia.user_modified= self.request.user
        guia.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:manifest-detail',
                kwargs={'pk': guia.manifest.pk },
            )
        )

        return super(GuideUpdateView, self).form_valid(form)


class GuideDetailView(DetailView):
    '''
    vista para ver el detalle y lista de guas de una mnifiesto
    '''
    model = Guide
    template_name = 'recepcion/guide/detail.html'


class GuideDeleteView(DeleteView):
    model = Guide
    template_name = 'recepcion/guide/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:manifest-detail',
                kwargs={'pk': self.object.manifest.pk },
            )
        )


class GuideDelete(DeleteView):
    model = Guide
    template_name = 'recepcion/guide/delete2.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            reverse(
                'cliente_app:cliente-filter_guide',
            )
        )


class ReceptionGuideView(FormView):
    '''
    vista para recepcionar guias de un manifiesto
    '''
    template_name = 'recepcion/manifest/reception.html'
    form_class = ReceptionForm
    success_url = reverse_lazy('recepcion_app:manifest-list')

    def get_context_data(self, **kwargs):
        context = super(ReceptionGuideView, self).get_context_data(**kwargs)
        manifiesto_pk = self.kwargs.get('pk', 0)
        context['manifiesto'] = Manifest.objects.get(pk=manifiesto_pk)
        return context

    def get_form_kwargs(self):
        kwargs = super(ReceptionGuideView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs.get('pk', 0),
        })
        return kwargs

    def form_valid(self, form):
        guias = form.cleaned_data['guide']
        for guia in guias:
            guia.state = '1'
            guia.date_reception = datetime.now()
            guia.save()

        return super(ReceptionGuideView, self).form_valid(form)


#mantenimientos para la tabla observaciones
class ObsCreateView(CreateView):
    '''
    vista para agregar una nueva observacion
    '''
    model = Observations
    form_class = ObservationsForm
    template_name = 'recepcion/obs/add.html'

    def get_context_data(self, **kwargs):
        context = super(ObsCreateView, self).get_context_data(**kwargs)
        context['guide'] = self.kwargs.get('pk', 0)
        return context

    def form_valid(self, form):
        obs = form.save(commit=False)
        #recuperamos la guia
        guide_pk = self.kwargs.get('pk', 0)
        guia = Guide.objects.get(pk=guide_pk)
        obs.guide = guia
        obs.user_created = self.request.user
        obs.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:guide-update',
                kwargs={'pk': guide_pk },
            )
        )


class ObsUpdateView(UpdateView):
    '''
    vista para modificar una observacion
    '''
    model = Observations
    template_name = 'recepcion/obs/update.html'
    form_class = ObservationsForm
    success_url = reverse_lazy('recepcion_app:obs-list')

    def form_valid(self, form):
        form.save()
        obs = self.get_object()
        obs.user_modified = self.request.user
        obs.save()

        return super(ObsUpdateView, self).form_valid(form)


class ObsDeleteView(DeleteView):
    '''
    vista para eliminar una Obaservacion
    '''
    model = Observations
    success_url = reverse_lazy('recepcio_app:obs-list')
    template_name = 'recepcion/obs/delete.html'


class ObsListView(ListView):
    '''
        muestra la lista de Observaciones
    '''
    context_object_name = 'list_obs'
    template_name = 'recepcion/obs/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ObsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("number", '')
        queryset = Observations.objects.guides(q)
        return queryset


class FilterView(ListView):
    '''
    vista para mostrar Reporte de Guias
    '''
    context_object_name = 'list_guide'
    paginate_by = 20
    template_name = 'recepcion/guide/filter.html'

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context['form'] = FilterForm
        return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("numero", '')
        r = self.request.GET.get("tipo", '')
        s = self.request.GET.get("date", '')
        queryset = Guide.objects.filtro_guides(q,r,s)
        return queryset


class ReportGuides(SingleObjectMixin, View):
    model = Guide

    def get(self, request, *args, **kwargs):
        #recuperamos el valor por GET
        q = self.request.GET.get("numero", '')
        r = self.request.GET.get("tipo", '')
        s = self.request.GET.get("date", '')
        guides = Guide.objects.filtro_guides(q,r,s)
        return generar_pdf(
            'recepcion/guide/print.html',
            {'pagesize' : 'A4', 'guides' : guides}
        )
