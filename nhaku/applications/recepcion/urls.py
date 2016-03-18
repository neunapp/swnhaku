from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^reception/manifest/list$',
        views.ManifestListView.as_view(),
        name='manifest-list'
    ),
    url(
        r'^reception/manifest/add$',
        views.ManifestCreateView.as_view(),
        name='manifest-add'
    ),
    url(
        r'^reception/manifest/update/(?P<pk>\d+)/$',
        views.ManifestUpdateView.as_view(),
        name='manifest-update'
    ),
    url(
        r'^reception/manifest/detail/(?P<pk>\d+)/$',
        views.ManifestDetailView.as_view(),
        name='manifest-detail'
    ),
    url(
        r'^reception/manifest/delete/(?P<pk>\d+)/$',
        views.ManifestDeleteView.as_view(),
        name='manifest-delete'
    ),
]
