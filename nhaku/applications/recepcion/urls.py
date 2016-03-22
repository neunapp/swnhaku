from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^reception/zone/list$',
        views.ZoneListView.as_view(),
        name='zone-list'
    ),
    url(
        r'^reception/zone/add$',
        views.ZoneCreateView.as_view(),
        name='zone-add'
    ),
    url(
        r'^reception/zone/update/(?P<pk>\d+)/$',
        views.ZoneUpdateView.as_view(),
        name='zone-update'
    ),
    url(
        r'^reception/zone/delete/(?P<pk>\d+)/$',
        views.ZoneDeleteView.as_view(),
        name='zone-delete'
    ),
    #urls para manifiesto
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
    #url para recepcion
    url(
        r'^reception/manifest/reception/(?P<pk>\d+)/$',
        views.ReceptionGuideView.as_view(),
        name='guide-reception'
    ),
]
