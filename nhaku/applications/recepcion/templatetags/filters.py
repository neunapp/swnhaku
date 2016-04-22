from django import template


register = template.Library()


@register.filter(name='split_label_recepcion')
#sepra un texto por el caracter guion
def split_label_recepcion(value):
    arreglo = value.split('*')
    arreglo[4] = str(round(float(arreglo[4])))+' Kg'
    print arreglo[4]
    return arreglo


@register.filter(name='split_label')
#sepra un texto por el caracter guion
def split_label(value):
    arreglo = value.split('*')
    print '==================='
    arreglo[4] = str(round(float(arreglo[4])))+' Kg'
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

@register.filter(name='peso_convert')
def peso_convert(value):
    return round(value)
