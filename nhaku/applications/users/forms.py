# -*- encoding: utf-8 -*-
from django import forms
# from .models import User

from django.contrib.auth import authenticate

from .models import User

class LoginForm(forms.Form):

    username = forms.CharField(
        label='usuario',
        max_length='30',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'autofocus': 'autofocus',
            }
        ),
    )
    password = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
            }
        ),
    )

    # def clean(self):
    #     cleaned_data = super(LoginForm, self).clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #
    #     print username, password
    #
    #     if not authenticate(username=username, password=password):
    #         raise forms.ValidationError('usuario o contraseña es incorrecta ..!!')
    #     return self.cleaned_data


class UserForm(forms.ModelForm):

    password1 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
            }
        ),
    )
    password2 = forms.CharField(
        label='contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
            }
        ),
    )

    class Meta:
        model = User
        fields = (
        )

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
