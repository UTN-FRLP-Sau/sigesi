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
                    confirmar_documentacion,
                    inscriptor_home
                    )

urlpatterns = [
    path('info', ConfirmacionInformacion.as_view(), name='confirmacion_info'),
    path('doc/upload', EntregarDocumentacion.as_view(), name='documentacion_subir'),
    path('doc/view/<pk>', MostrarDocumentacion.as_view(), name='documentacion_mostrar'),
    path('doc/confirm/', confirmar_documentacion, name='documentacion_confirmar'),
    #path('doc/delete/<pk>', rechazar_documentacion, name='documentacion_confirmar'),
    #path('doc/edit/<pk>', ConfirmarDocumentacion.as_view(), name='documentacion_confirmar'),
    path('doc/list/<str:aprobada>/', ListarDocumentacion.as_view(), name='documentacion_listar'),
    path('home', inscriptor_home, name='inscriptor_home'),
]
