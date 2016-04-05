# -*- encoding: utf-8 -*-
from django import forms


class SearchForm(forms.Form):
    '''
    formulario para buscar guas entregadas
    '''
    number = forms.CharField(
        label='Numero de Guia',
        max_length='20',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingrese Numero de Guia'
            }
        )
    )
    def clean_number(self):
        numero = self.cleaned_data['number']
        if not numero.isdigit():
            raise forms.ValidationError("Ingrese solo numeros por favor")
        return numero


class FilterForm(forms.Form):
    TIPO_CHOICES = (
        ('0', 'Guias No Entregadas'),
        ('1', 'Guias No Recepcionadas'),
        ('2', 'Guias Con Observacion'),
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control input-sm'
            }
        )
    )


class PanelForm(forms.Form):
    date = forms.DateField(
        'Fecha',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }
        )
    )
