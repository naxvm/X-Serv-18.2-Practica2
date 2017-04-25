from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import get_template
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from acorta.models import UrlDB 

# Create your views here.

@csrf_exempt  # Para poder hacer el POST.
def main(request):
    if request.method == 'GET':
        ans = 'Hola. Has hecho un GET. <br><br>'
        home = ('http://localhost:' + request.get_host() + '/')

        if UrlDB.objects.all().exists():
            ans += 'Aquí están las URLs ya acortadas: <br>'
            lista = UrlDB.objects.all()
            for direccion in lista:
                link = home + str(direccion.id)
                long_link = direccion.larga

                ans += ('<br><a href="' + link + '">' + link + '</a>' +
                        ' → ' + '<a href="' + long_link + '">' + long_link +
                        '</a>')
                
    
        
        else:
            ans += ('La base de datos de URLs está vacía. ' +
                    '<b>¡Añade la primera!</b><br>')

        formulario = ('<br><br><center><form method="post">' +
                        'Introduce tu URL:<br>' +
                        '<input type="text" name="url">' +
                        '<input type="submit" value="Acortar">' +
                        '</form></center>')

        ans += formulario	

    else:  # POST
        ans = 'Hola. Has hecho un POST.<br>'
        recv = urllib.parse.unquote(request.POST['url'])
        # Añadimos el 'http://' en caso de no ser así
        print(recv[0:8])
        if recv[0:7] != 'http://' and recv[0:8] != 'https://':
            recv = 'http://' + recv
        
        if recv in UrlDB.objects.all():
            short = recv.id
        else:
            new_element = UrlDB(larga=recv)
            new_element.save()
            short = (home + str(new_element.id))
            ans += ('<br><a href=">' + short + '">' + short + '</a>' +
                 ' → ' + '<a href=">' + recv + '">' + recv + '</a>')




    return HttpResponse(ans)


def goto(request, argument):
    # Intentaremos extraer el id. Si falla, ejecutamos el método de error.
    try:
        link = UrlDB.objects.get(id=int(argument)).larga

        return HttpResponseRedirect(link)
    except UrlDB.DoesNotExist:
        # Si no está, llamamos a error para que nos devuelva la página de error enlazando al inicio
        response = error(request)
        return response
    

def error(request):
    home = ('http://localhost:' + request.get_host() + '/')

    ans = ('<head><b>Error: recurso no encontrado</b></head>. <br><br>' +
            '<a href="' + home + '">Volver al inicio</a>')
    return HttpResponseBadRequest(ans)




