from django import forms

from applications.recepcion.models import Observations

class ObservationsForm(forms.ModelForm):
    # TODO: Define other fields here

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
