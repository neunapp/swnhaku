from __future__ import unicode_literals
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

# Create your models here.


@python_2_unicode_compatible
class Zone(TimeStampedModel):
    name = models.CharField(
        'Denominacion',
        max_length=100
    )
    state = models.BooleanField(default=True)
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


@python_2_unicode_compatible
class Manifest(TimeStampedModel):

    TYPE_CHOICES = (
        ('0', 'Aereo'),
        ('1', 'Juridico'),
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

@python_2_unicode_compatible
class Guide(TimeStampedModel):

    TYPE_CHOICES = (
        ('1', 'Oficina'),
        ('2', 'Reparto'),
    )
    PRIORITY_CHOISES = (
        ('1', 'Alta'),
        ('2', 'Media'),
        ('3', 'Baja'),
    )
    STATE_CHOISES = (
        ('1', 'En Oficina'),
        ('2', 'En Vehiculo'),
        ('3', 'Entregado'),
    )

    manifest = models.ForeignKey(Manifest)
    number = models.CharField(
        'Numero',
        max_length=11
    )
    number_objects = models.IntegerField(
        'Numero de Objetos',
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
    zona = models.ForeignKey(Zone)
    address = models.CharField(
        'Direccion',
        max_length=50
    )
    province = models.CharField(
        'Distrito-Provincia',
        max_length=50
    )
    priority = models.CharField(
        'Prioridad',
        max_length=2,
        choices=PRIORITY_CHOISES
    )
    type_guide = models.CharField(
        'Tipo de Envio',
        max_length=2,
        choices=TYPE_CHOICES
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

class Observations(TimeStampedModel):

    guide = models.ForeignKey(Guide)
    image = models.ImageField(
        'Imagen',
        upload_to="observations"
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
        editable=False
    )

    def __str__(self):
        return str(self.guide)
