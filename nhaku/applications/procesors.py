from applications.profiles.models import Client, Driver, Employee

def image_user(request):
    if not request.user.is_anonymous():
        usuario = request.user
        if Client.objects.filter(user=usuario).exists():
            ruta = Client.objects.get(
                user=usuario,
            ).avatar.url
        elif Driver.objects.filter(user=usuario).exists():
            ruta = Driver.objects.get(
                user=usuario,
            ).avatar.url

        elif Employee.objects.filter(user=usuario).exists():
            ruta = Employee.objects.get(
                user=usuario,
            ).avatar.url
        else:
            ruta = '/static/img/usuario.png'

        imagen = {'IMAGEN':ruta}
        return imagen
    else:
        imagen = {'IMAGEN':'/static/img/usuario.png'}
        return imagen
