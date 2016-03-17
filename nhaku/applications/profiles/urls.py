from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^perfiles/cliente/list$',
        views.ClientListView.as_view(),
        name='cliente-list'
    ),
    url(
        r'^perfiles/cliente/add$',
        views.ClientRegister.as_view(),
        name='cliente-add'
    ),
    url(
        r'^perfiles/cliente/update/(?P<pk>\d+)/$',
        views.ClientUpdateView.as_view(),
        name='cliente-update'
    ),
    url(
        r'^perfiles/cliente/detail/(?P<pk>\d+)/$',
        views.ClientDetailView.as_view(),
        name='cliente-detail'
    ),
    url(
        r'^perfiles/cliente/delete/(?P<pk>\d+)/$',
        views.ClientDeleteView.as_view(),
        name='cliente-delete'
    ),
]
