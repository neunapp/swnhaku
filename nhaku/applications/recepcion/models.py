from __future__ import unicode_literals
from model_utils.models import TimeStampedModel
from django.utils import timezone

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime, timedelta

# Create your models here.


@python_2_unicode_compatible
class Zone(TimeStampedModel):
    name = models.CharField(
        'Denominacion',
        max_length=100
    )
    state = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="zone_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="zone_modified",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name



class ManagerManifest(models.Manager):
    def manifest_by_day(self):
        #lista de manifiestos por dia
        return self.filter(
            date__day = timezone.now().day,
            state = False
        )

    def manifest_and_guide(self, user, fecha):
        tz = timezone.get_current_timezone()

        if fecha:
            date = datetime.strptime(fecha, "%d/%m/%Y")
            end_date = timezone.now()
            start_date = timezone.make_aware(date, tz)
        else:
            end_date = end_date = timezone.now()
            start_date = end_date - timedelta(days=5)

        manifiestos = self.filter(
            user=user,
            state=False,
            created__range=(start_date, end_date),
        )
        return manifiestos


@python_2_unicode_compatible
class Manifest(TimeStampedModel):

    TYPE_CHOICES = (
        ('0', 'Aereo'),
        ('1', 'Terrestre'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    number = models.CharField(
        'Numero',
        max_length=10
    )
    origin = models.CharField(
        'Origen',
        max_length=30
    )
    destination = models.CharField(
        'Destino',
        max_length=30
    )
    matricula = models.CharField(
        'Matricula/Placa',
        max_length=8
    )
    cargo = models.CharField(
        'Cargo',
        blank=True,
        max_length=8
    )
    date = models.DateTimeField(
        'Fech-Hora',
        default=datetime.now
    )
    type_manifest = models.CharField(
        'Tipo de Manifiesto',
        max_length=2,
        choices=TYPE_CHOICES
    )
    state = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="manifest_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="manifest_modified",
        blank=True,
        null=True,
    )

    objects = ManagerManifest()

    def __str__(self):
        return self.number


class ManagerGuide(models.Manager):
    def by_manifest(self, manifiesto):
        return self.filter(
            manifest=manifiesto,
            anulate=False,
        )

    def delete_guides(self, manifiesto, usuario):
        guides = self.filter(
            manifest=manifiesto,
            anulate=False,
        )
        for guia in guides:
            guia.anulate = True
            guia.user_modified = usuario
            guia.save()
        return True

    def zones_by_guide(self):
        #recuperamos la lista de guias
        guias = self.filter(
            state='1',
            anulate=False,
        )
        #creamos la variable de lista de zonas
        zonas = []
        for guia in guias:
            if (guia.zona) and (not guia.zona in zonas):
                zonas.append(guia.zona)

        return zonas

    def guide_deliver(self, number):
        tz = timezone.get_current_timezone()
        if number:

            return self.filter(
                number__icontains=number,
                state='4',
                anulate=False,
            ).order_by('date_reception')
        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=60)

            return self.filter(
                state='4',
                created__range=(start_date, end_date),
                anulate=False,
            ).order_by('date_reception')


    def no_deliver(self, value):
        if value == '0':
            queryset = self.filter(
                anulate=False,
            ).exclude(state='4')
        elif value == '1':
            queryset = self.filter(
                state='0',
                anulate=False,
            )
        else:
            lista_g = self.filter(
                anulate=False
            ).exclude(state='4')
            queryset = []
            lista_o = Observations.objects.all()
            for obs in lista_o:
                if obs.guide in lista_g:
                    queryset.append(obs.guide)

        return queryset



@python_2_unicode_compatible
class Guide(TimeStampedModel):

    TYPE_CHOICES = (
        ('0', 'Oficina'),
        ('1', 'Reparto'),
    )
    PRIORITY_CHOISES = (
        ('0', 'Alta'),
        ('1', 'Media'),
        ('2', 'Baja'),
    )
    STATE_CHOISES = (
        ('0', 'Sin Asignar'),
        ('1', 'En Oficina'),
        ('2', 'En Asignacion'),
        ('3', 'En Vehiculo'),
        ('4', 'Entregado'),
    )

    manifest = models.ForeignKey(Manifest)
    number = models.CharField(
        'Numero',
        max_length=11
    )
    number_objects = models.PositiveIntegerField(
        'Numero de Objetos',
        blank=True,
        null=True,
    )
    adreessee = models.CharField(
        'Remitente',
        max_length=50
    )
    weigth = models.DecimalField(
        'Peso',
        max_digits=7,
        decimal_places=3
    )
    content = models.CharField(
        blank=True,
        max_length=100
    )
    zona = models.ForeignKey(
        Zone,
        blank=True,
        null=True
    )
    address = models.CharField(
        'Direccion',
        max_length=50,
        blank=True,
    )
    province = models.CharField(
        'Distrito-Provincia',
        max_length=50,
        blank=True,
    )
    priority = models.CharField(
        'Prioridad',
        max_length=2,
        choices=PRIORITY_CHOISES,
        blank=True,
    )
    type_guide = models.CharField(
        'Tipo de Envio',
        max_length=2,
        choices=TYPE_CHOICES,
        blank=True,
    )
    date_reception = models.DateTimeField(
        blank=True,
        null = True,
        default=datetime.now
    )
    state = models.CharField(
        'Estado',
        max_length=2,
        choices=STATE_CHOISES
    )
    amount = models.DecimalField(
        'Monto',
        max_digits=7,
        decimal_places=3,
        blank=True,
        null=True,
    )
    date_deliver = models.DateTimeField(
        'Fecha de Entrega',
        blank=True,
        null=True
    )
    person_id = models.CharField(
        'Dni Receptor',
        blank=True,
        max_length=8
    )
    person_name = models.CharField(
        'Nombre Receptor',
        blank=True,
        max_length=30
    )
    anulate = models.BooleanField(
        'Anulado',
        default=False
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="guide_modified",
        blank=True,
        null=True,
    )

    objects = ManagerGuide()

    def __str__(self):
        return self.number


class ManagerObs(models.Manager):
    def guides(self, number):
        tz = timezone.get_current_timezone()
        if number:

            return self.filter(
                guide__number__icontains=number,
                guide__anulate=False,
            ).exclude(guide__state='4')
        else:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)

            return self.filter(
                created__range=(start_date, end_date),
                guide__anulate=False,
            ).exclude(guide__state='4')


class Observations(TimeStampedModel):

    TYPE_CHOICES = (
        ('0', 'Condicion de Paquete'),
        ('1', 'Perdida Guia'),
        ('2', 'perdida Paquete'),
        ('3', 'perdida Paquete'),
    )

    guide = models.ForeignKey(Guide)
    image = models.ImageField(
        'Imagen',
        upload_to="observations",
        blank=True,
        null=True,
    )
    type_observation = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
    )
    description = models.TextField(blank=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="observations_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="observations_modified",
        blank=True,
        null=True,
    )

    objects = ManagerObs()

    def __str__(self):
        return str(self.guide)
