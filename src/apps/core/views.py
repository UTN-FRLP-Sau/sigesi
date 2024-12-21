# Librerias Standars
from datetime import date

from django.shortcuts import render
from django.views.defaults import page_not_found, server_error
#from django.template import RequestContext

from apps.inscripcion.models import Curso

# Create your views here.


def landing_page(request):
    request.session['dni_verificado'] = False
    request.session['credencial'] = None
    hoy = date.today()  # hoy
    proximo_curso = Curso.objects.filter(
        inscripcion_inicio__gte=hoy).order_by('inscripcion_inicio').first()
    ultimo_curso = Curso.objects.filter(
        inscripcion_cierre__lte=hoy).order_by('inscripcion_cierre').last()
    context={}
    if proximo_curso:
        context['inicio_inscripcion'] = proximo_curso.inscripcion_inicio
        context['final_inscripcion'] = proximo_curso.inscripcion_cierre
    else:
        context['inicio_inscripcion'] = False
        context['final_inscripcion'] = ultimo_curso.inscripcion_cierre

    return render(request, 'landing/index.html', context=context)

# Error 404
def Error_404(request, exception):
    return render(request, 'error/404.html', status=404)

# Error 500
def Error_500(request):
    return render(request, 'error/500.html', status=500)
