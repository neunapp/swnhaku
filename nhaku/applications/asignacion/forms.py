# -*- encoding: utf-8 -*-
from django import forms

from .models import Car, Asignation

from applications.profiles.models import Driver
from applications.recepcion.models import Zone, Guide

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


class AsignationForm(forms.ModelForm):
    '''
    formulario para registrar asignacion
    '''

    class Meta:
        model = Asignation
        fields = (
            'driver',
            'assistant',
            'car',
        )

    def __init__(self, *args, **kwargs):
        super(AsignationForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.filter(state=False)
        self.fields['assistant'].queryset = Driver.objects.filter(state=False)
        self.fields['car'].queryset = Car.objects.filter(state=False)


class AddAsignationForm(forms.Form):
    '''
    formulario para añadir guias a una asignacion
    '''
    guide = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, pk, *args, **kwargs):
        super(AddAsignationForm, self).__init__(*args, **kwargs)
        # recuperamos el manifiesto
        guias = Guide.objects.filter(zona__pk=pk, anulate=False, state='1')
        self.fields['guide'].queryset = guias
        self.fields['guide'].label_from_instance = \
            lambda obj: "%s - %s - %s - %s - %s" % (
                obj.number,
                obj.number_objects,
                obj.adreessee,
                obj.content,
                obj.weigth,
            )
