from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from applications.users.views import Eror404View

handler404 = Eror404View.get_rendered_view()
handler500 = Eror404View.get_rendered_view()
urlpatterns = [
    url(r'^', include('applications.users.urls', namespace="users_app")),
    url(r'^', include('applications.profiles.urls', namespace="profiles_app")),
    url(r'^', include('applications.recepcion.urls', namespace="recepcion_app")),
    url(r'^', include('applications.asignacion.urls', namespace="asignacion_app")),
    url(r'^', include('applications.entrega.urls', namespace="entrega_app")),
    url(r'^', include('applications.clientes.urls', namespace="cliente_app")),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + '/static/img/logo.png')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
