# -*- encoding: utf-8 -*-
from django import forms

from .models import Client
from applications.users.models import User

class ClientForm(forms.ModelForm):
    '''
    Formulario para registrar usuario y cliente
    '''
    user_name = forms.CharField(
        label='usuario',
        max_length='30',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'nombre de usuario',
                'autofocus': 'autofocus',
            }
        ),
    )
    password1 = forms.CharField(
        label='contraseña',
        max_length=12,
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
                'placeholder': 'Ingrese contraseña',
            }
        ),
    )
    password2 = forms.CharField(
        label=' repetir contraseña',
        max_length=12,
        widget=forms.PasswordInput(
            attrs={
                'class': 'validate',
                'placeholder': 'Vuelva a ingresa la contraseña',
            }
        ),
    )

    class Meta:
        model =Client
        fields = (
            'full_name',
            'number_doc',
            'address',
            'email',
            'phone',
            'web',
            'avatar',
            'type_clint',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres o Razon Social',
                }
            ),
            'number_doc': forms.TextInput(
                attrs={
                    'placeholder': 'N° Doc.',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Direccion',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'E-mail',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Telefonos o Celular',
                }
            ),
            'web': forms.TextInput(
                attrs={
                    'placeholder': 'Direccion Pagina Web',
                }
            ),
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'validate',
                }
            ),
            'type_clint': forms.Select(
                attrs={
                    'class': 'form-control input-sm',
                }
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'las contraseñas no coinciden..!!')
        elif len(password2) < 5:
            print 'menor a 5 caracteres'
            self.add_error(
                'password2',
                'la contraseña debe tener por lo menos 5 caracteres!!'
            )
        else:
            return password2

    def clean_number_doc(self):
        number_doc = self.cleaned_data['number_doc']

        if not number_doc.isdigit():
            msj = 'el N° Documento solo deben contener numeros'
            self.add_error('number_doc', msj)
        elif len(number_doc) != 8 and len(number_doc) != 11:
            msj = 'el Dni o Ruc solo admiten 8 u 11 digitos'
            self.add_error('number_doc', msj)
        else:
            return number_doc

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        username_exist = User.objects.filter(username=user_name)

        if username_exist.count() > 0:
            msj = 'el nombre de usuario ya existe'
            self.add_error('user_name',msj)
        elif len(user_name) < 6:
            msj = 'la contraseña debe tener mas de 5 caracteres'
            self.add_error('user_name', msj)
        else:
            return user_name

    def clean_address(self):
        address = self.cleaned_data['address']

        if len(address) < 8:
            msj = 'La Direccion no es Valdia'
            self.add_error('address', msj)
        else:
            return address


class ClientUpdateForm(forms.ModelForm):
    '''
        formulario para actualizar datos de cliente
    '''

    class Meta:
        model =Client
        fields = (
            'full_name',
            'number_doc',
            'address',
            'email',
            'phone',
            'web',
            'avatar',
            'type_clint'
        )
