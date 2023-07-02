# future

# Librerias Standars

# Librerias de Terceros

# Django
from typing import Optional, Type
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

# Django Locales
from .forms import PersonaForm, EntregarDocumentacionForm
from .models import Persona, Estudiante, Pais, Documentacion
from .decorators import group_required

# Create your views here.


class EntregarDocumentacion(CreateView):
    template_name = 'documentacion/create.html'
    form_class = EntregarDocumentacionForm
    model = Documentacion
    #success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return render(self.request, 'documentacion/success.html')


class ConfirmacionInformacion(TemplateView):
    template_name = "documentacion/info.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required('inscriptor',), name='dispatch')
class MostrarDocumentacion(DetailView):
    template_name = 'documentacion/view.html'
    model = Documentacion
    context_object_name='objeto'


@method_decorator(login_required, name='dispatch')
@method_decorator(group_required('inscriptor',), name='dispatch')
class ListarDocumentacion(ListView):
    template_name = 'documentacion/list.html'
    model = Documentacion
    context_object_name='aspirantes'


def informacion_inscripcion(request):
        return render(request, 'info.html')


def persona_create(request):
    # Verificamos que el methodo sea POST
    if request.method == 'POST':
        # Si el methodo es POST, obtenemos el formulario
        form = PersonaForm(request.POST)
        # Verificamos si el Formulario es valido
        print(form.is_valid())
        if form.is_valid():
            # Si es valido, instaciamos los datos del modelo Persona:
            person = Persona(
                nombres = form.cleaned_data['nombre'],
                apellidos = form.cleaned_data['apellido'],
                fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
                pais_nacimiento = Pais.objects.get(nombre=form.cleaned_data['pais_nacimiento']),
                nacionalidad = Pais.objects.get(pk=form.cleaned_data['pais_nacionalidad']),
                documento_tipo = form.cleaned_data['documento_tipo'],
                numero_documento = form.cleaned_data['documento_numero'],
                domicilio_calle = form.cleaned_data['domicilio_calle'],
                domicilio_cpa = form.cleaned_data['domicilio_cp'],
                telefono = form.cleaned_data['telefono'],
                correo = form.cleaned_data['correo_1']
            )
            #Instanciamos el modelo Estudiante
            estudent = Estudiante(
                sexo = form.cleaned_data['sexo'],
                genero = form.cleaned_data['genero'],
                escuela = form.cleaned_data['escuela'],
                especialidad = form.cleaned_data['especialidad'],
                persona = person
            )
            # Guardamos la instancia del modelo en la DB
            person.save()
            estudent.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            form = PersonaForm()
            context =({
                'formulario': form,
                })
    else:
        form = PersonaForm()
        context =({
            'formulario': form,
            })
    return render (request, 'persona_create.html', context)


'''
				# Creamos el User de Django
				u = User.objects.create_user(
											username = form.cleaned_data['nickname'],
											email = form.cleaned_data['email'],
											password = form.cleaned_data['password1'],
											last_name = form.cleaned_data['apellido'],
											first_name = form.cleaned_data['nombre'],
											)
				# Lo agregamos al grupo alumnos
				u.groups.add(grupo_alumno)
				# Instanciamos a usuarios.Alumno
				a = Alumno(
					user = u,
					fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
					dni = form.cleaned_data['dni'],
					legajo = form.cleaned_data['legajo'],
					#comision = form.cleaned_data['comision'],
					carrera = form.cleaned_data['especialidad'],
					timestamp = datetime.now(),
					)
				u.save() # Guardamos Django.User
				a.save() # Guardamos usuarios.Alumno
				print (a)
				print (u)
				# Retornamos el formulrio para crear otro alumno
				return HttpResponseRedirect(reverse('usuario:crear_alumno'))
			else:
				print ('algo no anda')

		else:
			form = Fomulario_Creacion_Alumno()

		context =({
			'formulario': form,
		})

		return render (request, 'alumno/crear.html', context)

	# Si no es laboratorista
	else:
		# Redireccionamos al "Home"
		return HttpResponseRedirect(reverse('home'))
'''
