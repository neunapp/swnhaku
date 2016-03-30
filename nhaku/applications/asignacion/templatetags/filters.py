from django import template

from applications.recepcion.models import Observations


register = template.Library()


@register.filter(name='split_label')
#sepra un texto por el caracter guion
def split_label(value):
    arreglo = value.split('-')
    '''cadena = str(arreglo[5])
    if cadena == '0':
        arreglo[5] = 'ALTA'
    elif cadena == '1':
        arreglo[5] = 'MEDIA'
    else:
        arreglo[5] = 'BAJA'
        '''
    return arreglo

#muestra la cantidad de observaciones de una guia
@register.filter(name='count_observation')
def count_observation(value):
    count = Observations.objects.filter(guide__pk=value).count()
    return count
