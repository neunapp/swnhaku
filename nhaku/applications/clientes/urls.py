from django.conf.urls import url
from . import views

urlpatterns = [
    url(
    #urls para entrega
        r'^cliente/guias/buscar/$',
        views.SearchView.as_view(),
        name='cliente-search_guide'
    ),
    url(
    #urls para panel de cliente
        r'^cliente/panel/index/$',
        views.PanelView.as_view(),
        name='cliente-index'
    ),
    url(
    #urls para histora de una guia
        r'^cliente/panel/history/(?P<pk>\d+)/$',
        views.GuideHistoryView.as_view(),
        name='cliente-history'
    ),
    url(
    #urls para ir a perfil de usuario
        r'^cliente/panel/perfil/$',
        views.ProfileClient.as_view(),
        name='cliente-perfil'
    ),
    url(
    #urls para ir a perfil de usuario
        r'^cliente/guias/report/(?P<pk>\d+)/$',
        views.GuideByClient.as_view(),
        name='cliente-guias'
    ),
]
