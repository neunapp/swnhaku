from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^asignation/car/list$',
        views.CarListView.as_view(),
        name='car-list'
    ),
    url(
        r'^asignation/car/add$',
        views.CarRegister.as_view(),
        name='car-add'
    ),
    url(
        r'^asignation/car/update/(?P<pk>\d+)/$',
        views.CarUpdateView.as_view(),
        name='car-update'
    ),
    url(
        r'^asignation/car/detail/(?P<pk>\d+)/$',
        views.CarDetailView.as_view(),
        name='car-detail'
    ),
    url(
        r'^asignation/car/delete/(?P<pk>\d+)/$',
        views.CarDeleteView.as_view(),
        name='car-delete'
    ),
]
