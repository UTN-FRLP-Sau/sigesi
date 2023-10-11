# future

# Librerias Standars

# Librerias de Terceros

# Django
import threading
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView, View

# Django Locales
from .forms import EntregarDocumentacionForm, CreatePersonaForm, CreateStudentForm, VerificacionInscripcionForm, SubirDocumentacion
from .models import Documentacion, Persona, Estudiante
from .decorators import group_required

#Funciones generales
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


# Create your views here.
class EntregarDocumentacion(CreateView):
    template_name = 'documentacion/create.html'
    form_class = EntregarDocumentacionForm
    model = Documentacion

    def form_valid(self, form):
        form.save()
        return render(self.request, 'documentacion/success.html')


class ConfirmacionInformacion(TemplateView):
    template_name = "inscripcion\confirmacion_correo.html"


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
    paginate_by = 20
    context_object_name='aspirantes'

    def get(self, *args, **kwargs):
        if kwargs['aprobada']=='all':
            self.object_list = Documentacion.objects.all()
        else:
            queryset = Documentacion.objects.filter(aprobada=kwargs['aprobada'])
            if queryset.exists():
                self.object_list = Documentacion.objects.filter(aprobada=kwargs['aprobada'])
            else:
                return HttpResponseRedirect(reverse("documentacion_listar", args=['all']))
        context = self.get_context_data()
        context['estado'] = kwargs['aprobada']
        return self.render_to_response(context)


login_required
group_required('inscriptor',)
def confirmar_documentacion(request):
    if request.method == "POST":
        #Si es POST, obtenemos lo parametros del fomrulario
        doc_id = request.POST['id']
        opcion = request.POST['opcion']
        estado = request.POST['estado']
        if opcion == 'si':
            # Como la opcion es si, se le aprueba la documentacion.
            # Obtenemos la instacia de la documentacion
            doc = Documentacion.objects.get(pk=doc_id)
            # Se modifica el atributo aprobado a True
            doc.aprobada =True
            # Antes de guardar la instancia enviamos el correo con la confirmacion
            try:
                email=create_email(
                    user_mail=doc.correo,
                    subject='Confirmación de Inscripción',
                    template_name='documentacion/confirmacion_correo.html',
                    context={}
                    )
                thread = threading.Thread(target=email.send)
                thread.start()
                doc.save()
            except:
                messages.error(request, 'El correo no se a podido enviar, reintente mas tarde. Si el problema persiste, contacte con el administrador')
            # Retornamos a la vista actual
            return HttpResponseRedirect(reverse("documentacion_listar", args=[estado]))
        else:
            # Como la opcion no es si, se le rechaza la documentacion.
            # Obtenemos la instacia de la documentacion
            doc = Documentacion.objects.get(pk=doc_id)
            # Se modifica el atributo aprobado a True
            doc.aprobada = False
            # Se guarda la instancia
            doc.save()
            # Retornamos a la vista actual
            return HttpResponseRedirect(reverse("documentacion_listar", args=[estado]))
    else:
        return HttpResponseRedirect(reverse("inscriptor_home"))
    #documento = Documentacion.objects.get(pk=pk)
    #pass


@login_required
@group_required('inscriptor',)
def inscriptor_home(request):
    presentadas = Documentacion.objects.all().count()
    procesadas = Documentacion.objects.values('aprobada').filter(aprobada='True').count()
    faltantes = presentadas - procesadas
    porcientos = round(100*procesadas/presentadas,1)
    #Tarea.object.values("estado").filter(estado="Completado").count()
    context={
        'presentadas': presentadas,
        'procesadas': procesadas,
        'faltantes': faltantes,
        'porcientos': porcientos,
    }
    return render(request, 'usuario/home.html', context)


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
            persona = persona_form.save(commit=False)  # Guarda la instancia de persona sin guardar en la base de datos
            persona.save()  # Ahora persona tiene un ID asignado
            estudiante = estudiante_form.save(commit=False)  # Guarda la instancia de estudiante sin guardar en la base de datos
            estudiante.persona = persona  # Asigna la persona al estudiante
            estudiante.save()  # Guarda el estudiante en la base de datos
            try:
                email=create_email(
                    user_mail=persona.correo,
                    subject='Confirmación de Inscripción',
                    template_name='inscripcion/confirmacion_correo.html',
                    context={
                        'nombre': persona.nombres.title(),
                        'apellido': persona.apellidos.upper(),
                        'id_estudiante': estudiante.pk,
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
    fields=['especialidad','turno','modalidad']
    #form_class = TuFormularioDeActualizacion # Define tu formulario de actualización aquí
    # Resto de configuraciones como `success_url`, `fields`, etc.

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario ha pasado por VerificarDniView
        if not request.session.get('dni_verificado'):
            id_estudiante = self.kwargs['pk']
            return HttpResponseRedirect(reverse('verificar_dni', kwargs={'id_estudiante': id_estudiante}))
        else:
            pass
            #request.session['dni_verificado'] = False
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar dos instancias del formulario subirDocumentacion al contexto
        context['documento'] = SubirDocumentacion()
        context['certificado'] = SubirDocumentacion()
        return context












class ConfirmarInscripcion(CreateView):
    template_name = 'inscripcion/create.html'

    def get(self, request):
        contexto = {
            'documento_doc': EntregarDocumentacionForm(),
            'certificado_doc': EntregarDocumentacionForm()
        }
        return render(request, self.template_name, contexto)

    def form_valid(self, form):
        form.save()
        return render(self.request, 'documentacion/success.html')






class CrearEstudiante(View):
    template_name = 'inscripcion/create_student.html'

    def get(self, request, persona_id):
        estudiante_form = CreateStudentForm()
        return render(request, self.template_name, {'form': estudiante_form})

    def post(self, request, persona_id):
        persona = Persona.objects.get(pk=persona_id)
        estudiante_form = CreateStudentForm(request.POST)
        if estudiante_form.is_valid():
            with transaction.atomic():
                estudiante = estudiante_form.save(commit=False)
                estudiante.persona = persona
                estudiante.save()
            return render(self.request, 'inscripcion/success.html')
        return render(request, self.template_name, {'form': estudiante_form})
