from django.http import JsonResponse

from .models import (Provincia, PartidoPBA, Localidad)

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
    options = '<option value="" selected="selected">---------</option>'
    response = {}
    if provincia_id == '6':
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


def get_localidades(request):
    partido_id = request.GET.get('domicilio_partido')
    options = '<option value="" selected="selected">---------</option>'
    response = {}
    if partido_id:
        localidades = Localidad.objects.filter(partido=partido_id)
        for localidad in localidades:
            options += '<option value="{}">{}</option>'.format(
                localidad.pk,
                localidad.nombre.title()
            )
    response['localidades'] = options
    return JsonResponse(response)
