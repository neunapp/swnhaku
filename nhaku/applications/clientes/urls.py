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
    #urls para reportes
        r'^cliente/guias/reporte/$',
        views.FilterView.as_view(),
        name='cliente-filter_guide'
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
]
