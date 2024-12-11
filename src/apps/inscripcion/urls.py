# future

# Librerias Standars

# Librerias de Terceros

# Django
from django.urls import path
from django.views.generic import TemplateView


# Django Locales
from .views import (#ConfirmacionInformacion,
                    #EntregarDocumentacion,
                    #MostrarDocumentacion,
                    #ListarDocumentacion,
                    VerificacionInscripcion,
                    CreatePersonaAndEstudent,
                    ActualizarInscripcionView,
                    #confirmar_documentacion,
                    #inscriptor_home,
                    InscripcionCerrada,
                    ReenvioLinkdocumentacion,
                    CursosView,
                    CreateInscripcionView,
                    SubirDoc,
                    UpdateInscripcionView,
                    EstudianteListView,
                    aprobar_curso,
                    export_user_asistentes_to_excel,
                    inscribir_curso
                    )
from .ajax import get_provincias, get_partidos, get_localidades, get_escuelas

urlpatterns = [
    #path('info', ConfirmacionInformacion.as_view(), name='confirmacion_info'),
    #path('doc/upload', EntregarDocumentacion.as_view(), name='documentacion_subir'),
    #path('doc/view/<pk>', MostrarDocumentacion.as_view(), name='documentacion_mostrar'),
    #path('doc/confirm/', confirmar_documentacion, name='documentacion_confirmar'),
    #path('doc/delete/<pk>', rechazar_documentacion, name='documentacion_confirmar'),
    #path('doc/edit/<pk>', ConfirmarDocumentacion.as_view(), name='documentacion_confirmar'),
    #path('doc/list/<str:aprobada>/', ListarDocumentacion.as_view(), name='documentacion_listar'),
    #path('home', inscriptor_home, name='inscriptor_home'),

    #De aqui en mas es el nuevo sistema
    path('nueva/preinscripcion/', CreatePersonaAndEstudent.as_view(), name='crear_persona'),
    #path('nueva/preinscripcion/', InscripcionCerrada.as_view(), name='crear_persona'),
    path('verificar-doc/<int:id_estudiante>/', VerificacionInscripcion.as_view(), name='verificar_doc'),
    path('verificar-dni/<int:id_estudiante>/', VerificacionInscripcion.as_view(), name='verificar_dni'),
    path('paso-2/<int:pk>/', CursosView.as_view(), name='paso_2'),
    path('paso-2/documentacion/', SubirDoc.as_view(), name='subir_documentacion'),
    path('incribirse/', CreateInscripcionView.as_view(), name='crear_inscripcion'),
    path('actualizar/', UpdateInscripcionView.as_view(), name='actualizar_inscripcion'),
    #path('reenvio/correo', ReenvioLinkdocumentacion.as_view(),name='inscripcion_info'),
    path('info', ReenvioLinkdocumentacion.as_view(), name='inscripcion_info'),
    #path('new/student/<int:persona_id>/', CrearEstudiante.as_view(), name='crear_estudiante'),
    #path('new/student/success/', CrearEstudiante.as_view(), name='crear_estudiante_success'),

    #URL para Ajax
    path('ajax/new/person/get_provincias', get_provincias, name='get_provincias'),
    path('ajax/new/person/get_partidos', get_partidos, name='get_partidos'),
    path('ajax/new/person/get_localidades', get_localidades, name='get_localidades'),
    path('ajax/new/person/get_escuelas', get_escuelas, name='get_escuelas'),
    
    #URL para la administracion
    path('administracion', TemplateView.as_view(template_name = "admin/home.html"), name='home_administracion'),
    path('administracion/estudiantes/', EstudianteListView.as_view(), name='admin-estudiantes_list'),
    path('administracion/estudiantes/estado/ap',aprobar_curso, name='aprobar_curso'),
    path('exportar-inscriptos/', export_user_asistentes_to_excel, name='exportar_inscriptos'),
    path('inscribir_en_curso/', inscribir_curso, name='inscribir_en_curso'),
]
