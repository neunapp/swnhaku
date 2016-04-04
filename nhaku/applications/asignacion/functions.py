from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import cStringIO as StringIO

import ho.pisa as pisa

def generar_pdf(template_scr, context_dict):
    template = get_template(template_scr)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf') 
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
