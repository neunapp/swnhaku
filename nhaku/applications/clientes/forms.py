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
