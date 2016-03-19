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
    #urls para tabla Guide
    url(
        r'^reception/guide/add/(?P<pk>\d+)/$',
        views.GuideCreateView.as_view(),
        name='guide-add'
    ),
    url(
        r'^reception/guide/update/(?P<pk>\d+)/$',
        views.GuideUpdateView.as_view(),
        name='guide-update'
    ),
    url(
        r'^reception/guide/detail/(?P<pk>\d+)/$',
        views.GuideDetailView.as_view(),
        name='guide-detail'
    ),
    url(
        r'^reception/guide/delete/(?P<pk>\d+)/$',
        views.GuideDeleteView.as_view(),
        name='guide-delete'
    ),
]
