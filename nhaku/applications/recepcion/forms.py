# -*- encoding: utf-8 -*-
from django import forms

from .models import Manifest

class ManifestForm(forms.ModelForm):

    class Meta:
        model = Manifest
        fields = (
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
