from django.conf.urls import url
from . import views

urlpatterns = [
    url(
    #urls para entrega
        r'^cliente/guias/buscar/$',
        views.SearchView.as_view(),
        name='cliente-search_guide'
    ),
]
