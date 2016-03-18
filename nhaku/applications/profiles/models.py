from __future__ import unicode_literals
from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Client(TimeStampedModel):

    TYPE_CHOICES = (
            ('0', 'Juridica'),
            ('1', 'Natural'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    full_name = models.CharField(
        'nombres/razon social',
        max_length=100
    )
    number_doc = models.CharField(
        'dni/ruc',
        max_length=100
    )
    address = models.CharField(
        'direccion',
        max_length=100
    )
    email = models.EmailField()
    phone = models.CharField(
        'telefono',
        blank=True,
        max_length=15
    )
    mobil = models.CharField(
        'celular',
        blank=True,
        max_length=15
    )
    web = models.URLField(
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to="cliente",
    )
    type_clint = models.CharField(
        'Tipo de Cliente',
        max_length=2,
        choices=TYPE_CHOICES
    )
    state = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="Client_created",
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="client_modified",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.full_name


@python_2_unicode_compatible
class Driver(TimeStampedModel):

    GENDER_CHOICES = (
        ('M', 'masculino'),
        ('F', 'femenino'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.CharField(
        'nombres',
        max_length=40
    )
    last_name = models.CharField(
        'apellidos',
        max_length=40
    )
    dni = models.CharField(
        'DNI',
        max_length=8
    )
    email = models.EmailField(
        blank=True,
        null=True
    )
    phone = models.CharField(
        'telefono/celular',
        blank=True,
        max_length=100
    )
    address = models.CharField(
        'direccion',
        max_length=100
    )
    gender = models.CharField(
        'sexo',
        max_length=1,
        choices=GENDER_CHOICES
    )
    date_birth = models.DateField(
        'fecha de nacimiento',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to="driver",
    )
    license = models.CharField(
        'licencia',
        blank=True,
        max_length=11
    )
    class_driver = models.CharField(
        'Clase de licencia',
        blank=True,
        max_length=2
    )
    category = models.CharField(
        blank=True,
        max_length=2
    )
    state = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="driver_created",
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="driver_modified",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.first_name

@python_2_unicode_compatible
class Employee(TimeStampedModel):

    GENDER_CHOICES = (
        ('M', 'masculino'),
        ('F', 'femenino'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.CharField(
        'nombres',
        max_length=40
    )
    last_name = models.CharField(
        'apellidos',
        max_length=40
    )
    dni = models.CharField(
        'DNI',
        max_length=8
    )
    email = models.EmailField(
        blank=True,
        null=True
    )
    phone = models.CharField(
        'telefono/celular',
        blank=True,
        max_length=100
    )
    address = models.CharField(
        'direccion',
        max_length=100
    )
    gender = models.CharField(
        'sexo',
        max_length=1,
        choices=GENDER_CHOICES
    )
    date_birth = models.DateField(
        'fecha de nacimiento',
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to="driver",
        blank=True,
        null=True
    )
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="employee_created",
    )
    user_modified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="employee_modified",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.first_name
