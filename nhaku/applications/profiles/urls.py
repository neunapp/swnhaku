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
    #urls para Conductores
    url(
        r'^perfiles/driver/list$',
        views.DriverListView.as_view(),
        name='driver-list'
    ),
    url(
        r'^perfiles/driver/add$',
        views.DriverCreateView.as_view(),
        name='driver-add'
    ),
    url(
        r'^perfiles/driver/update/(?P<pk>\d+)/$',
        views.DriverUpdateView.as_view(),
        name='driver-update'
    ),
    url(
        r'^perfiles/driver/detail/(?P<pk>\d+)/$',
        views.DriverDetailView.as_view(),
        name='driver-detail'
    ),
    url(
        r'^perfiles/driver/delete/(?P<pk>\d+)/$',
        views.DriverDeleteView.as_view(),
        name='driver-delete'
    ),
    # urls para Empelados
    url(
        r'^perfiles/employee/list$',
        views.EmployeeListView.as_view(),
        name='employee-list'
    ),
    url(
        r'^perfiles/employee/add$',
        views.EmployeeCreateView.as_view(),
        name='employee-add'
    ),
    url(
        r'^perfiles/employee/update/(?P<pk>\d+)/$',
        views.EmployeeUpdateView.as_view(),
        name='employee-update'
    ),
    url(
        r'^perfiles/employee/detail/(?P<pk>\d+)/$',
        views.EmployeeDetailView.as_view(),
        name='employee-detail'
    ),
    url(
        r'^perfiles/employee/delete/(?P<pk>\d+)/$',
        views.EmployeeDeleteView.as_view(),
        name='employee-delete'
    ),
    url(
        r'^dashboard/$',
        views.Dashboard.as_view(),
        name='dashboard'
    ),
]
