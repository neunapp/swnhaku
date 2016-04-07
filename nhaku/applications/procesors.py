from applications.profiles.models import Client, Driver, Employee

def image_user(request):
    if not request.user.is_anonymous():
        usuario = request.user
        ruta = '/static/img/usuario.png'
        if Client.objects.filter(user=usuario).exists():
            cliente = Client.objects.get(
                user=usuario,
            )
            if cliente.avatar:
                ruta = cliente.avatar.url
            else:
                ruta = '/static/img/usuario.png'

        elif Driver.objects.filter(user=usuario).exists():
            driver = Driver.objects.get(
                user=usuario,
            )
            if driver.avatar:
                ruta = driver.avatar.url
            else:
                ruta = '/static/img/usuario.png'

        elif Employee.objects.filter(user=usuario).exists():
            employee = Employee.objects.get(
                user=usuario,
            )
            if employee.avatar:
                ruta = employee.avatar.url
            else:
                ruta = '/static/img/usuario.png'

        else:
            ruta = '/static/img/usuario.png'

        imagen = {'IMAGEN':ruta}
        return imagen
    else:
        imagen = {'IMAGEN':'/static/img/usuario.png'}
        return imagen
