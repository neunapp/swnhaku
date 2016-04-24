from django import template

from applications.recepcion.models import Observations, Guide
from applications.asignacion.models import DetailAsignation

register = template.Library()

@register.filter(name='split_label_recepcion')
#sepra un texto por el caracter guion
def split_label_recepcion(value):
    arreglo = value.split('*')
    arreglo[4] = str(arreglo[4])+' Kg'
    print arreglo[4]
    return arreglo


@register.filter(name='split_label')
#sepra un texto por el caracter guion
def split_label(value):
    arreglo = value.split('*')
    print '==================='
    print '**** peso ****'
    print arreglo[4]
    '''
    alto = 0
    medio = 1

    if alto == arreglo[5]:
        print '**** alto ***'
        arreglo[5] = 'Alta'
    elif medio == arreglo[5]:
        print '**** media ***'
        arreglo[5] = 'Medio'
    else:
        print '**** bajo ***'
        arreglo[5] = 'Baja'
    '''
    arreglo[5] = arreglo[5] + ' Dias'
    return arreglo

#muestra la cantidad de observaciones de una guia
@register.filter(name='count_observation')
def count_observation(value):
    count = Observations.objects.filter(
        guide__pk=value,
        guide__anulate=False,
    ).count()
    return count


#devuleve las guias entregadas (entregados/total)
@register.filter(name='deliver_guides')
def deliver_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_deliver = 0
    for g in guias:
        if g.state == '4':
            num_deliver = num_deliver + 1

    return '('+str(num_deliver)+'/'+str(guias.count())+')'


#cuenta las guias observadas de un manifiesto
@register.filter(name='obs_guides')
def obs_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_obs = 0
    for g in guias:
        if Observations.objects.filter(guide=g, type_observation='0').exclude(guide__state='4').exists():
            num_obs = num_obs + 1

    return num_obs


#clase para lamacenar datos de guia y observacion
class DetailGuia():
    guia = None
    asignacion = None
    observacion = None

# devuelve una lista de objetos de tio DetailGuia
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

@register.filter(name='peso_convert')
def peso_convert(value):
    return str(value)
