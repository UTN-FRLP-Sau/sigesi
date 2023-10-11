# future

# Librerias Standars

# Librerias de Terceros

# Django
from django.urls import path

# Django Locales
from .views import (ConfirmacionInformacion,
                    EntregarDocumentacion,
                    MostrarDocumentacion,
                    ListarDocumentacion,
                    CreatePersona,
                    VerificacionInscripcion,
                    CrearEstudiante,
                    ActualizarUsuarioView,
                    confirmar_documentacion,
                    inscriptor_home
                    )
from .ajax import get_provincias, get_partidos, get_localidades

urlpatterns = [
    path('info', ConfirmacionInformacion.as_view(), name='confirmacion_info'),
    path('doc/upload', EntregarDocumentacion.as_view(), name='documentacion_subir'),
    path('doc/view/<pk>', MostrarDocumentacion.as_view(), name='documentacion_mostrar'),
    path('doc/confirm/', confirmar_documentacion, name='documentacion_confirmar'),
    #path('doc/delete/<pk>', rechazar_documentacion, name='documentacion_confirmar'),
    #path('doc/edit/<pk>', ConfirmarDocumentacion.as_view(), name='documentacion_confirmar'),
    path('doc/list/<str:aprobada>/', ListarDocumentacion.as_view(), name='documentacion_listar'),
    path('home', inscriptor_home, name='inscriptor_home'),

    #De aqui en mas es el nuevo sistema
    path('new/person/', CreatePersona.as_view(), name='crear_persona'),
    path('verificar-dni/<int:id_estudiante>/', VerificacionInscripcion.as_view(), name='verificar_dni'),
    path('actualizar-usuario/<int:pk>/', ActualizarUsuarioView.as_view(), name='paso_2'),
    #path('new/student/<int:persona_id>/', CrearEstudiante.as_view(), name='crear_estudiante'),
    #path('new/student/success/', CrearEstudiante.as_view(), name='crear_estudiante_success'),

    #URL para Ajax
    path('ajax/new/person/get_provincias', get_provincias, name='get_provincias'),
    path('ajax/new/person/get_partidos', get_partidos, name='get_partidos'),
    path('ajax/new/person/get_localidades', get_localidades, name='get_localidades'),
]
