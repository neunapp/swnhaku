from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^reception/manifest/add$',
        views.ManifestCreateView.as_view(),
        name='manifest-add'
    ),
]
