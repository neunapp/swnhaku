# -*- encoding: utf-8 -*-
from django import forms

from applications.users.models import User

from .models import Manifest, Guide, Zone


class ZoneForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de la Zonas',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Zone.objects.filter(name=name, state=False).count() > 0:
            msj = 'el nombre de zona ya existe'
            self.add_error('name', msj)
        return name


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
        }

    def clean(self):
        cleaned_data = super(GuideForm, self).clean()
        number = cleaned_data.get('number')
        guia = Guide.objects.filter(number=number, anulate=False).exists()
        if guia:
            message = "la guia de remision %s ya existe" % (number)
            self.add_error('number', message)
        return cleaned_data

    def clean_number(self):
        number = self.cleaned_data['number']

        arreglo = number.split('-')
        for a in arreglo:
            if not a.isdigit():
                msj = 'El Numero de Guia no puede contener Letras'
                print msj
                self.add_error('number', msj)
            else:
                return number

    def clean_weigth(self):
        weigth = self.cleaned_data['weigth']

        if weigth < 0:
            msj = 'no es un valor valido para peso'
            self.add_error('weigth', msj)
        else:
            return weigth


class GuideUpdateForm(forms.ModelForm):
    '''
    formulario para modificar guias de remisions
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
            'amount',
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
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Monto a Cobrar',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GuideUpdateForm, self).__init__(*args, **kwargs)
        zona = Zone.objects.filter(state=False)
        self.fields['zona'].queryset = zona

    def clean_number(self):
        number = self.cleaned_data['number']

        arreglo = number.split('-')
        for a in arreglo:
            if not a.isdigit():
                msj = 'El Numero de Guia no puede contener Letras'
                print msj
                self.add_error('number', msj)
            else:
                return number

    def clean_weigth(self):
        weigth = self.cleaned_data['weigth']

        if weigth < 0:
            msj = 'no es un valor valido para peso'
            self.add_error('weigth', msj)
        else:
            return weigth


# formulario para confirmar recepcion
class ReceptionForm(forms.Form):
    '''
    formulario para confirmar Recepcion
    '''
    guide = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, pk, *args, **kwargs):
        super(ReceptionForm, self).__init__(*args, **kwargs)
        # recuperamos el manifiesto
        guias = Guide.objects.filter(manifest__pk=pk, anulate=False, state='0')
        self.fields['guide'].queryset = guias
        self.fields['guide'].label_from_instance = \
            lambda obj: "%s * %s * %s * %s * %s" % (
                obj.number,
                obj.number_objects,
                obj.adreessee,
                obj.content,
                obj.weigth,
            )


class FilterForm(forms.Form):
    TIPO_CHOICES = (
        ('0', 'Guias Registradas'),
        ('1', 'Guias No Entregadas'),
        ('2', 'Guias Perdidas'),
        ('3', 'Guias No Recepcionadas'),
    )
    numero = forms.CharField(
        label='Numero',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numero de Guia',
            }
        )
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control input-sm'
            }
        )
    )
    date = forms.DateField(
        'Fecha',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker',
                'placeholder': 'ingrese Fecha de Nacimiento',
            },
            format='%d/%m/%Y'
        )
    )
