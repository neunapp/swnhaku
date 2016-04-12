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
        if g.state == '3':
            num_asg = num_asg + 1
    return num_asg

#devuelve numero de guias en oficina
def OfficeGuides(value):
    #recuperamos lista de guias
    guias = Guide.objects.by_manifest(value)
    num_office = 0
    for g in guias:
        if g.state == '1':
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
