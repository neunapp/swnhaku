# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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
from applications.asignacion.functions import generar_pdf, guide_by_zone

from datetime import datetime

# Create your views here.

class ZoneCreateView(LoginRequiredMixin, CreateView):
    '''
    vista para registrar zona nueva
    '''
    model = Zone
    form_class = ZoneForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:zone-list')
    template_name = 'recepcion/zone/add.html'

    def get_context_data(self, **kwargs):
        context = super(ZoneCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            return context

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.user_created = self.request.user
        zona.save()

        return super(ZoneCreateView, self).form_valid(form)


class ZoneUpdateView(LoginRequiredMixin, UpdateView):
    '''
    vista para modificar una zona
    '''
    model = Zone
    template_name = 'recepcion/zone/update.html'
    form_class = ZoneForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:zone-list')

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
        form.save()
        zona = self.get_object()
        zona.user_modified = self.request.user
        zona.save()

        return super(ZoneUpdateView, self).form_valid(form)


class ZoneDeleteView(LoginRequiredMixin, DeleteView):
    '''
    vista para desabilitar una zona
    '''
    model = Zone
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:zone-list')
    template_name = 'recepcion/zone/delete.html'

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
        self.object.state = True
        self.object.user_modified = self.request.user
        self.object.save()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class ZoneListView(LoginRequiredMixin, ListView):
    '''
        muestra la lista de zonas
    '''
    context_object_name = 'zone_list'
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/zone/list.html'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            #recuperamos el valor por GET
            queryset = Zone.objects.filter(state=False)
            return queryset


class Zone_by_GuideListView(LoginRequiredMixin, ListView):
    '''
    lista de zonas que corresponden a guias en oficina
    '''
    context_object_name = 'zone_list'
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/zone/by_guides.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(Zone_by_GuideListView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            asignation_pk = self.kwargs.get('pk', 0)
            context['asignacion'] = Asignation.objects.get(pk=asignation_pk)
            return context

    def get_queryset(self):
        #recuperamos el valor por GET
        zones = Guide.objects.zones_by_guide()
        queryset = guide_by_zone(zones)
        return queryset


class ManifestCreateView(LoginRequiredMixin, CreateView):
    '''
    vista para crear un manifiesto
    '''
    model = Manifest
    form_class = ManifestForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:manifest-list')
    template_name = 'recepcion/manifest/add.html'

    def get_context_data(self, **kwargs):
        context = super(ManifestCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            return context

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


class ManifestUpdateView(LoginRequiredMixin, UpdateView):
    '''
    vista para actualizar un manifiesto
    '''
    model = Manifest
    template_name = 'recepcion/manifest/update.html'
    form_class = ManifestForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:manifest-list')

    def get_context_data(self, **kwargs):
        context = super(ManifestUpdateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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

class ManifestDetailView(LoginRequiredMixin, DetailView):
    '''
    vista para ver el detalle y lista de guas de una mnifiesto
    '''
    model = Manifest
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/manifest/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ManifestDetailView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
            manifiesto = self.get_object()
            #listamos las guis de este manifiesto
            context['list_guias'] = Guide.objects.by_manifest(manifiesto)
            return context


class ManifestDeleteView(LoginRequiredMixin, DeleteView):
    '''
    metodo para eliminar o poner manifiesto en eliminado
    '''
    model = Manifest
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/manifest/delete.html'
    success_url = reverse_lazy('recepcion_app:manifest-list')

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
        self.object.state = True
        self.object.user_modified = self.request.user
        #eliminamos las guis del manifiesto
        Guide.objects.delete_guides(self.object, self.request.user)
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class ManifestListView(LoginRequiredMixin, ListView):
    '''
        muestra la lista de manifiestos
    '''
    context_object_name = 'manifest_list'
    template_name = 'recepcion/manifest/list.html'
    login_url = reverse_lazy('users_app:login')
    paginate_by = 20

    def get_queryset(self):
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            #recuperamos el valor por GET
            queryset = Manifest.objects.manifest_by_day()

        return queryset


class GuideCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    vista para registrar las guias de remision
    '''
    model = Guide
    form_class = GuideForm
    success_url = '.'
    template_name = 'recepcion/guide/add.html'
    login_url = reverse_lazy('users_app:login')
    success_message = "La Guia Se Guardo Correctamente..."

    def get_context_data(self, **kwargs):
        context = super(GuideCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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


class GuideUpdateView(LoginRequiredMixin, UpdateView):
    '''
    metodo para modificar y actualizar una guia
    '''
    model = Guide
    template_name = 'recepcion/guide/update.html'
    login_url = reverse_lazy('users_app:login')
    form_class = GuideUpdateForm
    success_url = '.'

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


class GuideDetailView(LoginRequiredMixin, DetailView):
    '''
    vista para ver el detalle y lista de guas de una mnifiesto
    '''
    model = Guide
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/guide/detail.html'

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


class GuideDeleteView(LoginRequiredMixin, DeleteView):
    model = Guide
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/guide/delete.html'

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
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:manifest-detail',
                kwargs={'pk': self.object.manifest.pk },
            )
        )


class GuideDelete(LoginRequiredMixin, DeleteView):
    model = Guide
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/guide/delete2.html'

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
        self.object.anulate = True
        self.object.user_modified = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            reverse(
                'recepcion_app:report-filter',
            )
        )


class ReceptionGuideView(LoginRequiredMixin, FormView):
    '''
    vista para recepcionar guias de un manifiesto
    '''
    template_name = 'recepcion/manifest/reception.html'
    form_class = ReceptionForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:manifest-list')

    def get_context_data(self, **kwargs):
        context = super(ReceptionGuideView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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
class ObsCreateView(LoginRequiredMixin, CreateView):
    '''
    vista para agregar una nueva observacion
    '''
    model = Observations
    form_class = ObservationsForm
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/obs/add.html'

    def get_context_data(self, **kwargs):
        context = super(ObsCreateView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
                raise Http404("No Se Encontro la Pagina")
        else:
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


class ObsUpdateView(LoginRequiredMixin, UpdateView):
    '''
    vista para modificar una observacion
    '''
    model = Observations
    template_name = 'recepcion/obs/update.html'
    form_class = ObservationsForm
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcion_app:obs-list')

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
        form.save()
        obs = self.get_object()
        obs.user_modified = self.request.user
        obs.save()

        return super(ObsUpdateView, self).form_valid(form)


class ObsDeleteView(LoginRequiredMixin, DeleteView):
    '''
    vista para eliminar una Obaservacion
    '''
    model = Observations
    login_url = reverse_lazy('users_app:login')
    success_url = reverse_lazy('recepcio_app:obs-list')
    template_name = 'recepcion/obs/delete.html'

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


class ObsListView(LoginRequiredMixin, ListView):
    '''
        muestra la lista de Observaciones
    '''
    context_object_name = 'list_obs'
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/obs/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ObsListView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            context['form'] = SearchForm
            return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("number", '')
        queryset = Observations.objects.guides(q)
        return queryset


class FilterView(LoginRequiredMixin, ListView):
    '''
    vista para mostrar Reporte de Guias
    '''
    context_object_name = 'list_guide'
    paginate_by = 20
    login_url = reverse_lazy('users_app:login')
    template_name = 'recepcion/guide/filter.html'

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        usuario = self.request.user
        if not (usuario.type_user == '4' or usuario.type_user == '1'):
            raise Http404("No Se Encontro la Pagina")
        else:
            context['form'] = FilterForm
            return context

    def get_queryset(self):
        #recuperamos el valor por GET
        q = self.request.GET.get("numero", '')
        r = self.request.GET.get("tipo", '')
        s = self.request.GET.get("date", '')
        queryset = Guide.objects.filtro_guides(q,r,s)
        return queryset


class ReportGuides(LoginRequiredMixin, SingleObjectMixin, View):
    model = Guide
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
            #recuperamos el valor por GET
            q = self.request.GET.get("numero", '')
            r = self.request.GET.get("tipo", '')
            s = self.request.GET.get("date", '')
            guides = Guide.objects.filtro_guides(q,r,s)
            return generar_pdf(
                'recepcion/guide/print.html',
                {'pagesize' : 'A4', 'guides' : guides}
            )
