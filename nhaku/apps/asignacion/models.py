from __future__ import unicode_literals
from model_utils.models import TimeStampedModel
"""
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime

from apps.recepcion.models import Guide

# Create your models here.

class Car(TimeStampedModel):

    model = models.CharField(
        'Modelo de Vehiculo',
        max_length=30
    )
    plaque = models.CharField(
        'Placa',
        max_length=7
    )
    marca = models.CharField(
        'Marca',
        max_length=20
    )
    phone = models.CharField(
        'Telefono Asignado',
        blank=True,
        max_length=15
    )
    code_settings_car = models.CharField(
        'codigo de configuracion vehicular',
        max_length=6
    )
    constancy_inscription = models.CharField(
        'Constancia de Inscripcion',
        max_length=12
    )
    state = models.BooleanField(
        'Estado',
        default=False
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="car_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="car_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return self.model


class Asignation(TimeStampedModel):

    STATE_CHOICES = (
        ('0', 'Asignado'),
        ('1', 'Salio'),
        ('2','Volvio'),
    )

    driver = models.ForeignKey(
        'Conductor',
        settings.AUTH_USER_MODEL,
        related_name="driver_asignation",
    )
    assistant = models.ForeignKey(
        'Ayudante',
        settings.AUTH_USER_MODEL,
        related_name="assistant_asignation",
        blank=True,
        null=True,
    )
    car = models.ForeignKey(
        'Vehiculo',
        Car
    )
    date_start = models.DateTimeField(
        'Fecha de Salida',
        blank=True,
        null=True,
        default=datetime.now
    )
    date_retunr = models.DateTimeField(
        'Fecha y Hora de Retorno',
        blank=True,
        null=True,
    )
    state = models.CharField(
        'Estado Asignacion',
        max_length=2,
        choices=STATE_CHOICES
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_created",
        #editable=False
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="asignation_modified",
        blank=True,
        null=True,
        editable=False
    )

    def __str__(self):
        return self.driver


class DetailAsignation(TimeStampedModel):

    asignation = models.ForeignKey(
        'Asignacion',
        Asignation
    )
    guide = models.ForeignKey(
        'Guia',
        Guide
    )
    state = models.BooleanField(
        'Estado',
        default=True
    )

    def __str__(self):
        return self.asignation

"""
