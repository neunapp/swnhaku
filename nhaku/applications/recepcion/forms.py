# -*- encoding: utf-8 -*-
from django import forms

from applications.users.models import User

from .models import Manifest, Guide

class ManifestForm(forms.ModelForm):

    class Meta:
        model = Manifest
        fields = (
            'user',
            'number',
            'origin',
            'destination',
            'matricula',
            'cargo',
            'date',
            'type_manifest',
        )
        widgets = {
            'number': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Manifiesto',
                }
            ),
            'origin': forms.TextInput(
                attrs={
                    'placeholder': 'Origen de Manifiesto',
                }
            ),
            'destination': forms.TextInput(
                attrs={
                    'placeholder': 'Destino de Arrivo',
                }
            ),
            'matricula': forms.TextInput(
                attrs={
                    'placeholder': 'Matricula o Placa de Vehiculo',
                }
            ),
            'cargo': forms.TextInput(
                attrs={
                    'placeholder': 'Vuelo o Salida',
                }
            ),
            'date': forms.TextInput(
                attrs={
                    'placeholder': 'Fecha de Recepcion',
                }
            ),
        }

        def clean_number(self):
            number = self.cleaned_data['number']

            if not number.isdigit():
                msj = 'Solo deben contener numeros'
                self.add_error('number', msj)
            else:
                return number

    def __init__(self, *args, **kwargs):
        super(ManifestForm, self).__init__(*args, **kwargs)
        usuarios = User.objects.filter(type_user='3', is_active=True)
        self.fields['user'].queryset = usuarios


class GuideForm(forms.ModelForm):
    '''
    formulario para registrar las guias de remision
    '''
    class Meta:
        model = Guide
        fields = (
            'number',
            'number_objects',
            'adreessee',
            'weigth',
            'content',
            'zona',
            'address',
            'province',
            'priority',
            'type_guide',
        )
        widgets = {
            'number': forms.TextInput(
                attrs={
                    'placeholder': 'Numero de Guia',
                }
            ),
            'number_objects': forms.NumberInput(
                attrs={
                    'placeholder': '00',
                }
            ),
            'adreessee': forms.TextInput(
                attrs={
                    'placeholder': 'Persona Remitente',
                }
            ),
            'weigth': forms.NumberInput(
                attrs={
                    'placeholder': 'Peso del Paquete',
                }
            ),
            'content': forms.TextInput(
                attrs={
                    'placeholder': 'Descripcion del Paquete',
                }
            ),
            'zona': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Direccion de Entrega',
                }
            ),
            'province': forms.TextInput(
                attrs={
                    'placeholder': 'procincia/Distriro',
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
            'type_guide': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            ),
        }

        def clean_number(self):
            number = self.cleaned_data['number']

            if not number.isdigit():
                msj = 'Solo debe contener numeros'
                self.add_error('number', msj)
            else:
                return number

        def clean_weigth(self):
            weigth = form.cleaned_data['weigth']

            if weigth < 0:
                msj = 'no es un valor valido para peso'
                self.add_error('weigth', msj)
            else:
                return weigth
