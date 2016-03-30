from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^entrega/asignation/reception/(?P<pk>\d+)/$',
        views.ReceptionAsignationView.as_view(),
        name='entrega-reception'
    ),
    #urls para observacion
    url(
        r'^entrega/observacion/add/(?P<as>\d+)/(?P<pk>\d+)/$',
        views.ObservationCreateView.as_view(),
        name='observation-add'
    ),
]
