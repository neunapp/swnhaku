# -*- encoding: utf-8 -*-
from django import forms

from .models import Car
from applications.users.models import User

class CarForm(forms.ModelForm):
    '''
    Formulario para registrar Vehiculos
    '''
    class Meta:
        model = Car
        fields = (
            'model',
            'plaque',
            'marca',
            'phone',
            'code_settings_car',
            'constancy_inscription',
        )
        widgets = {
            'model': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese una Denominacion'
                }
            ),
            'plaque': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de Placa'
                }
            ),
            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Marca del Vehiculo'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Marca del Vehiculo'
                }
            ),
            'code_settings_car': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Codigo de Configuracion Vehicular'
                }
            ),
            'constancy_inscription': forms.TextInput(
                attrs={
                    'class': 'form-control input-sm',
                    'placeholder': 'Ingrese Nro de Cosntacia de Inscripcion'
                }
            ),
        }
