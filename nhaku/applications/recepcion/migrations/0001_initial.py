# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 16:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=11, verbose_name='Numero')),
                ('number_objects', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero de Objetos')),
                ('adreessee', models.CharField(max_length=50, verbose_name='Remitente')),
                ('weigth', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='Peso')),
                ('content', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='Direccion')),
                ('province', models.CharField(blank=True, max_length=50, verbose_name='Distrito-Provincia')),
                ('priority', models.CharField(blank=True, choices=[('0', 'Alta'), ('1', 'Media'), ('2', 'Baja')], max_length=2, verbose_name='Prioridad')),
                ('type_guide', models.CharField(blank=True, choices=[('0', 'Oficina'), ('1', 'Reparto')], max_length=2, verbose_name='Tipo de Envio')),
                ('date_reception', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('state', models.CharField(choices=[('0', 'Sin Asignar'), ('1', 'En Oficina'), ('2', 'En Vehiculo'), ('3', 'Entregado')], max_length=2, verbose_name='Estado')),
                ('amount', models.DecimalField(blank=True, decimal_places=3, max_digits=7, verbose_name='Monto')),
                ('date_deliver', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Entrega')),
                ('person_id', models.CharField(blank=True, max_length=8, verbose_name='Dni Receptor')),
                ('person_name', models.CharField(blank=True, max_length=30, verbose_name='Nombre Receptor')),
                ('anulate', models.BooleanField(default=False, verbose_name='Anulado')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manifest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=10, verbose_name='Numero')),
                ('origin', models.CharField(max_length=30, verbose_name='Origen')),
                ('destination', models.CharField(max_length=30, verbose_name='Destino')),
                ('matricula', models.CharField(max_length=8, verbose_name='Matricula/Placa')),
                ('cargo', models.CharField(blank=True, max_length=8, verbose_name='Cargo')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fech-Hora')),
                ('type_manifest', models.CharField(choices=[('0', 'Aereo'), ('1', 'Terrestre')], max_length=2, verbose_name='Tipo de Manifiesto')),
                ('state', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', models.ImageField(upload_to='observations', verbose_name='Imagen')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Denominacion')),
                ('state', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
