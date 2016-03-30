from django.conf.urls import url
from . import views

urlpatterns = [
    url(
    #urls para entrega
        r'^entrega/asignation/reception/(?P<pk>\d+)/$',
        views.ReceptionAsignationView.as_view(),
        name='entrega-reception'
    ),
    url(
        r'^entrega/asignation/deliver/$',
        views.AsignationListView.as_view(),
        name='entrega-list_asignation'
    ),
    url(
        r'^entrega/asignation/deliver/guide/(?P<pk>\d+)/$',
        views.GuideByAsignation.as_view(),
        name='entrega-list_guides'
    ),
    url(
        r'^entrega/observacion/add/(?P<as>\d+)/(?P<pk>\d+)/$',
        views.DeliverView.as_view(),
        name='entrega-deliver'
    ),
    #urls para observacion
    url(
        r'^entrega/observacion/add/(?P<as>\d+)/(?P<pk>\d+)/$',
        views.ObservationCreateView.as_view(),
        name='observation-add'
    ),
    url(
        r'^entrega/observacion/add/deliver/(?P<as>\d+)/(?P<pk>\d+)/$',
        views.DeliverObservation.as_view(),
        name='observation-add_deliver'
    ),
]
