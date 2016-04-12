from django import template

from applications.recepcion.models import Observations, Guide
from applications.asignacion.models import DetailAsignation

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
    count = Observations.objects.filter(
        guide__pk=value,
        guide__anulate=False,
    ).count()
    return count


@register.filter(name='deliver_guides')
def deliver_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_deliver = 0
    for g in guias:
        if g.state == '4':
            num_deliver = num_deliver + 1

    return '('+str(num_deliver)+'/'+str(guias.count())+')'


@register.filter(name='obs_guides')
def obs_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_obs = 0
    for g in guias:
        if Observations.objects.filter(guide=g, type_observation='0').exclude(guide__state='4').exists():
            num_obs = num_obs + 1

    return str(num_obs)


#clase para lamacenar datos de guia y observacion
class DetailGuia():
    guia = None
    asignacion = None
    observacion = None

@register.filter(name='iterar_guides')
def iterar_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    lista = []
    for g in guias:
        obj_guia = DetailGuia()
        obj_guia.guia = g
        #recuperamos una asignacion
        if DetailAsignation.objects.filter(guide=g).exists():
            obj_guia.asignacion = DetailAsignation.objects.filter(
                guide=g,
            )[0].asignation
        #recuperamos la lista de observaciones
        if Observations.objects.filter(guide=g).exists():
            obj_guia.observacion = Observations.objects.filter(
                guide=g
            )[0]

        lista.append(obj_guia)

    return lista
