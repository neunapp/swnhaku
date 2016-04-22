from applications.recepcion.models import Observations, Guide
from applications.asignacion.models import DetailAsignation


#devuelve la cantidad de guias entregadas
def DeliverGuides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_deliver = 0
    for g in guias:
        if g.state == '4':
            num_deliver = num_deliver + 1
    return num_deliver

#devuelve numero de guias asignadas
def AsgGuides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_asg = 0
    for g in guias:
        if g.state == '3' or g.state == '2':
            num_asg = num_asg + 1
    return num_asg

#devuelve numero de guias en oficina
def OfficeGuides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_office = 0
    for g in guias:
        value_obs = Observations.objects.filter(guide=g,
            type_observation='0'
        ).exclude(guide__state='4').exists()

        if g.state == '1' and not value_obs:
            num_office = num_office + 1

    return num_office


#cuenta las guias observadas de un manifiesto
def obs_guides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_obs = 0
    for g in guias:
        if Observations.objects.filter(guide=g, type_observation='0').exclude(guide__state='4').exists():
            num_obs = num_obs + 1

    return num_obs


class ReporteGuia():
    entregadas = 0
    reparto = 0
    observacion = 0
    oficina = 0

#devuelve objectos de tipo ReporteGuia
def report_guides(value):
    #iteramos los manifiestos
    r = ReporteGuia()
    for m in value:
        r.observacion = r.observacion + obs_guides(m)
        r.entregadas = r.entregadas + DeliverGuides(m)
        r.reparto = r.reparto + AsgGuides(m)
        r.oficina = r.oficina + OfficeGuides(m)
        #iteramos las guias
    return r


class Histoy():
    tipo = None
    fecha = None
    objeto = None


#metodo para devolver la historia de una guia
def historia_guia(guia):
    #lista que contiene objetos de tipo Histoy
    lista = []
    #agregamos la primera historia
    h = Histoy()
    h.tipo = '0'
    h.fecha = guia.date_reception
    h.objeto = guia
    lista.append(h)
    #verificamos si existen asignaciones
    asignaciones = DetailAsignation.objects.filter(
        guide=guia,
        guide__anulate=False,
    )
    if asignaciones.count() > 0:
        #agregamos las asignaciones como historia
        for a in asignaciones:
            ha = Histoy()
            ha.tipo = '1'
            ha.fecha = a.created
            ha.objeto = a
            lista.append(ha)
    #verificamos si existen observaciones
    observaciones = Observations.objects.filter(
        guide=guia,
        guide__anulate=False,
    )
    if observaciones.count() > 0:
        #agregamos las observaciones como historia
        for obs in observaciones:
            ho = Histoy()
            ho.tipo = '2'
            ho.fecha = obs.created
            ho.objeto = obs
            lista.append(ho)
    #verificamos si fue observado y no entregado
    if asignaciones.count() > 0 and observaciones.count() > 0 and guia.state == '1':
        for a in asignaciones:
            he = Histoy()
            he.tipo = '0'
            he.fecha = a.asignation.date_retunr
            he.objeto = guia
            lista.append(he)

    lista2 = sorted(lista, key=lambda Histoy: Histoy.fecha)
    #devolvemos la lista ordenanda
    return lista2
