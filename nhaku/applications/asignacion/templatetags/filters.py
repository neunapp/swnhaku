from django import template

from applications.recepcion.models import Observations


register = template.Library()


@register.filter(name='split_label')
#sepra un texto por el caracter guion
def split_label(value):
    arreglo = value.split('*')

    return arreglo

#muestra la cantidad de observaciones de una guia
@register.filter(name='count_observation')
def count_observation(value):
    count = Observations.objects.filter(guide__pk=value).count()
    return count

@register.filter(name='peso_convert')
def peso_convert(value):
    return round(value)
