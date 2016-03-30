# -*- encoding: utf-8 -*-
from django import forms

from applications.recepcion.models import Observations

class ObservationsForm(forms.ModelForm):
    '''
    formulario para registrar nueva observacion
    '''
    class Meta:
        model = Observations
        fields = (
            'type_observation',
            'image',
            'description',
        )
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describa la observacion'
                }
            ),
        }

class DeliverForm(forms.Form):
    '''
    formulario para realizar entrega de paquete
    '''
    dni = forms.CharField(
        label='Dni Receptor',
        max_length=8,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese Dni',
            }
        )
    )
    full_name = forms.CharField(
        label='Nombre Completo',
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Ingrese Nombre Completo',
            }
        )
    )

    def clean_dni(self):
        dni = self.cleaned_data['dni']

        if not dni.isdigit():
            msj = 'el N° DNI solo debe contener numeros'
            self.add_error('dni', msj)
        elif len(dni) != 8:
            msj = 'el Dni solo admiten 8 digitos'
            self.add_error('dni', msj)
        else:
            return dni
