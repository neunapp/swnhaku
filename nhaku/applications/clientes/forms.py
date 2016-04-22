# -*- encoding: utf-8 -*-
from django import forms
from django.core.files.images import get_image_dimensions


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


class ProfileForm(forms.Form):

    password1 = forms.CharField(
        label='contraseña',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
            }
        ),
    )
    password2 = forms.CharField(
        label='contraseña',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repita la Contraseña',
            }
        ),
    )
    image = forms.ImageField(
        label='Imagen',
        required=False,
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'las contraseñas no coinciden..!!')
        elif len(password2) < 5 and len(password2) > 0:
            print 'menor a 5 caracteres'
            self.add_error(
                'password2',
                'la contraseña debe tener por lo menos 5 caracteres!!'
            )
        else:
            return password2
