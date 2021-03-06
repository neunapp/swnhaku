from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^asignation/car/list$',
        views.CarListView.as_view(),
        name='car-list'
    ),
    url(
        r'^asignation/car/add$',
        views.CarRegister.as_view(),
        name='car-add'
    ),
    url(
        r'^asignation/car/update/(?P<pk>\d+)/$',
        views.CarUpdateView.as_view(),
        name='car-update'
    ),
    url(
        r'^asignation/car/detail/(?P<pk>\d+)/$',
        views.CarDetailView.as_view(),
        name='car-detail'
    ),
    url(
        r'^asignation/car/delete/(?P<pk>\d+)/$',
        views.CarDeleteView.as_view(),
        name='car-delete'
    ),
    #urls para asignacion
    url(
        r'^asignation/asignation/list$',
        views.AsignationListView.as_view(),
        name='asignation-list'
    ),
    url(
        r'^asignation/asignation/add/$',
        views.AsignationCreateView.as_view(),
        name='asignation-add'
    ),
    url(
        r'^asignation/asignation/delete/(?P<pk>\d+)/$',
        views.AsignationDeleteView.as_view(),
        name='asignation-delete'
    ),
    url(
        r'^asignation/imprimir/asignacion/(?P<pk>\d+)/$',
        views.ReportAsigView.as_view(),
        name='asignation-print'
    ),
    #urls para el proceso de asignar desasignar guias
    url(
        r'^asignation/asignation/asignar_guide/(?P<as>\d+)/(?P<pk>\d+)/$',
        views.AddGuideAsignationView.as_view(),
        name='asignation-asignar_guide'
    ),
    url(
        r'^asignation/asignation/list_guide/(?P<pk>\d+)/$',
        views.GuideByAsignationListView.as_view(),
        name='asignation-list_guide'
    ),
    url(
        r'^asignation/asignar/confirmar/(?P<pk>\d+)/$',
        views.ConfirmarAsignationView.as_view(),
        name='asignation-confirmar'
    ),
    url(
        r'^asignation/asignar/delete/(?P<guide>\d+)/(?P<pk>\d+)/$',
        views.DeleteAsignationDeleteView.as_view(),
        name='asignation-detail_delete'
    ),
]
