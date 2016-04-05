from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^$',
        views.LogIn.as_view(),
        name='login'
    ),
    url(
        r'^users/salir/$',
        'applications.users.views.LogOut',
        name='user-salir'
    ),
    url(
        r'^users/usuario/update/(?P<pk>\d+)/$',
        views.UserUpdateView.as_view(),
        name='user-update'
    ),
]
