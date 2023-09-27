from django.http import JsonResponse

from .models import (Pais,
                     Provincia,
                     PartidoPBA,
                     Localidad
)


def get_provincias(request):
    pais_id = request.GET.get('domicilio_pais')
    provincias = Provincia.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if pais_id:
        provincias = Provincia.objects.filter(pais=pais_id)   
    for provincia in provincias:
        options += '<option value="{}">{}</option>'.format(
            provincia.pk,
            provincia.nombre.title()
        )
    response = {}
    response['provincias'] = options
    return JsonResponse(response)


def get_partidos(request):
    provincia_id = request.GET.get('domicilio_provincia')
    print(provincia_id)
    #partidos = PartidoPBA.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    response = {}
    if provincia_id == 6:
        partidos = PartidoPBA.objects.filter(provincia=provincia_id)
        for partido in partidos:
            options += '<option value="{}">{}</option>'.format(
                partido.pk,
                partido.nombre.title()
            )
        response['partidos'] = options
    else:
        localidades = Localidad.objects.filter(provincia=provincia_id)
        for localidad in localidades:
            options += '<option value="{}">{}</option>'.format(
                localidad.pk,
                localidad.nombre.title()
            )
        response['localidades'] = options
    return JsonResponse(response)
'''
def get_localidades(request):
    municipio_id = request.GET.get('municipio_id')
    localidades = Localidad.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if municipio_id:
        localidades = Localidad.objects.filter(municipio_id=municipio_id)   
    for localidad in localidades:
        options += '<option value="%s">%s</option>' % (
            localidad.pk,
            localidad.localidad
        )
    response = {}
    response['localidades'] = options
    return JsonResponse(response)
    
'''