# future

# Librerias Standars

# Librerias de Terceros

# Django
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template
from django.views.generic.edit import UpdateView
from django.views.generic import View, TemplateView

# Django Locales
from .forms import CreatePersonaForm, CreateStudentForm, VerificacionInscripcionForm, SubirDocumentoForm, SubirCertificadoForm, ActualizarInscripcionForm
from .models import Persona, Estudiante, Archivos

# Funciones generales


def create_email(user_mail, subject, template_name, context, request):
    template = get_template(template_name)
    content = template.render(context=context, request=request)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message

class InscripcionCerrada(TemplateView):
    template_name = "inscripcion/inscripcion_cerrada.html"

#####################################################################################################
#####################################################################################################
#####################################################################################################


class CreatePersonaAndEstudent(View):
    template_name = 'inscripcion/create_student.html'

    def get(self, request):
        contexto = {
            'persona_form': CreatePersonaForm(),
            'estudiante_form': CreateStudentForm()
        }
        return render(request, self.template_name, contexto)

    def post(self, request):
        persona_form = CreatePersonaForm(request.POST)
        estudiante_form = CreateStudentForm(request.POST)
        if persona_form.is_valid() and estudiante_form.is_valid():
            # Guarda la instancia de persona sin guardar en la base de datos
            persona = persona_form.save(commit=False)
            persona.save()  # Ahora persona tiene un ID asignado
            # Guarda la instancia de estudiante sin guardar en la base de datos
            estudiante = estudiante_form.save(commit=False)
            estudiante.persona = persona  # Asigna la persona al estudiante
            estudiante.save()  # Guarda el estudiante en la base de datos
            try:
                email = create_email(
                    user_mail=persona.correo,
                    subject='Confirmación de Inscripción',
                    template_name='inscripcion/confirmacion_correo.html',
                    context={
                        'nombre': persona.nombres.title(),
                        'apellido': persona.apellidos.upper(),
                        'id_estudiante': estudiante.pk,
                        'carrera': estudiante.especialidad,
                        'turno': estudiante.turno,
                        'modalidad': estudiante.modalidad
                    },
                    request=request
                )
                thread = threading.Thread(target=email.send)
                thread.start()
                return render(self.request, 'inscripcion/success.html')
            except:
                Estudiante.objects.filter(pk=estudiante.pk).delete()
                Persona.objects.filter(pk=persona.pk).delete()
        contexto = {
            'persona_form': persona_form,
            'estudiante_form': estudiante_form
        }
        return render(request, self.template_name, contexto)


class VerificacionInscripcion(View):
    form_class = VerificacionInscripcionForm
    template_name = 'inscripcion/verificar_dni.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            id_estudiante = self.kwargs['id_estudiante']
            try:
                estudiante = Estudiante.objects.get(credencial=id_estudiante)
                usuario = Persona.objects.get(id=estudiante.persona.id)
                if usuario.numero_documento == dni:
                    # Verificación exitosa, guardamos en la sesión
                    request.session['dni_verificado'] = True
                    return HttpResponseRedirect(reverse('paso_2', kwargs={'pk': id_estudiante}))
                else:
                    form.add_error('dni', 'El DNI no coincide con el usuario')
            except Persona.DoesNotExist:
                print(Exception)
                form.add_error(None, 'El usuario no existe')
        return render(request, self.template_name, {'form': form})


class ActualizarUsuarioView(UpdateView):
    model = Estudiante
    template_name = 'inscripcion/update.html'
    fields = ['especialidad', 'turno', 'modalidad']
    # form_class = ActualizarInscripcionForm

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario ha pasado por VerificarDniView
        if not request.session.get('dni_verificado'):
            id_estudiante = self.kwargs['pk']
            return HttpResponseRedirect(reverse('verificar_dni', kwargs={'id_estudiante': id_estudiante}))
        else:
            #request.session['dni_verificado']=False
            id_estudiante = self.kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar dos instancias del formulario subirDocumentacion al contexto
        estudiante = Estudiante.objects.get(pk=self.kwargs['pk'])
        archivos = Archivos.objects.filter(persona=estudiante.persona)
        if archivos.exists():
            documento = archivos.filter(tipo='Identificacion').last()
            certificado = archivos.filter(tipo='Certificado').last()
            if documento and documento.estado == 2:
                context['documento_form'] = SubirDocumentoForm(
                    prefix='documento')
                context['documento_info'] = False
            elif documento and documento.estado == 1:
                context['documento_form'] = False
                context['documento_info'] = 'si'
            elif documento and documento.estado == 0:
                context['documento_form'] = False
                context['documento_info'] = 'no'
            if certificado and certificado.estado == 2:
                context['certificado_info'] = False
                context['certificado_form'] = SubirCertificadoForm(
                    prefix='certificado')
            elif certificado and certificado.estado == 1:
                context['certificado_form'] = False
                context['certificado_info'] = 'si'
            elif certificado and certificado.estado == 0:
                context['certificado_form'] = False
                context['certificado_info'] = 'no'
        else:
            context['documento_form'] = SubirDocumentoForm(prefix='documento')
            context['certificado_form'] = SubirCertificadoForm(
                prefix='certificado')
        return context

    def post(self, request, *args, **kwargs):
        # Obtener las instacioas de los formualrios
        form_documento = SubirDocumentoForm(
            request.POST, request.FILES, prefix='documento')
        form_certificado = SubirCertificadoForm(
            request.POST, request.FILES, prefix='certificado')
        # Obtener la instancia del Estudiante que se está actualizando
        estudiante = self.get_object()
        # Obtener los datos del formulario
        especialidad = request.POST.get('especialidad')
        turno = request.POST.get('turno')
        modalidad = request.POST.get('modalidad')
        estudiante = Estudiante.objects.get(pk=self.kwargs['pk'])
        archivos = Archivos.objects.filter(persona=estudiante.persona)
        if archivos.exists():
            documento = archivos.filter(tipo='Identificacion').last()
            certificado = archivos.filter(tipo='Certificado').last()
            if documento and documento.estado == 2:
                if form_documento.is_valid():
                    # Guardar los datos del formulario
                    # Guarda la instancia sin guardar en la base de datos
                    documento = form_documento.save(commit=False)
                    documento.tipo = 'Identificacion'
                    documento.persona = estudiante.persona  # Asigna la persona
                    documento.save()  # Guarda en la base de datos
            if certificado and certificado.estado == 2:
                if form_certificado.is_valid():
                    # Guarda la instancia sin guardar en la base de datos
                    certificado = form_certificado.save(commit=False)
                    certificado.tipo = 'Certificado'
                    certificado.persona = estudiante.persona  # Asigna la persona
                    certificado.save()  # Guarda en la base de datos
            # Actualizar los campos del estudiante
            estudiante.especialidad = especialidad
            estudiante.turno = turno
            estudiante.modalidad = modalidad
            # Guardar los cambios en la base de datos
            estudiante.save()
            return self.form_valid(form_certificado)
        else:
            if form_documento.is_valid() and form_certificado.is_valid():  # and form.is_valid():
                estudiante = Estudiante.objects.get(pk=self.kwargs['pk'])
                # Guardar los datos del formulario
                # Guarda la instancia sin guardar en la base de datos
                documento = form_documento.save(commit=False)
                documento.tipo = 'Identificacion'
                documento.persona = estudiante.persona  # Asigna la persona
                documento.save()  # Guarda en la base de datos
                # Guarda la instancia sin guardar en la base de datos
                certificado = form_certificado.save(commit=False)
                certificado.tipo = 'Certificado'
                certificado.persona = estudiante.persona  # Asigna la persona
                certificado.save()  # Guarda en la base de datos
                # Actualizar los campos del estudiante
                estudiante.especialidad = especialidad
                estudiante.turno = turno
                estudiante.modalidad = modalidad
                # Guardar los cambios en la base de datos
                estudiante.save()
                return self.form_valid(form_certificado, form_documento)
            else:
                request.session['dni_verificado'] = True
                return self.form_invalid(form_certificado)

    def form_valid(self, form):
        return render(self.request, 'inscripcion/success2.html')
                # request.session['dni_verificado'] = True
#                return self.form_invalid(form_certificado, form_documento)

#    def form_valid(self, form_certificado, form_documento):
#        return render(self.request, 'inscripcion/success.html')

#    def form_invalid(self, form_certificado, form_documento):
#        # Lógica para el caso de formularios no válidos
#        # Devolver el contexto con los formularios y los errores de validación
#        context = self.get_context_data(
#            form_certificado=form_certificado, form_documento=form_documento)
#        return self.render_to_response(context)

