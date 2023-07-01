"""
URL configuration for sigesi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from .views import informacion_inscripcion, ConfirmacionInformacion, EntregarDocumentacion, MostrarDocumentacion, ListarDocumentacion

urlpatterns = [
    path('info', ConfirmacionInformacion.as_view(), name='confirmacion_info'),
    path('doc/upload', EntregarDocumentacion.as_view(), name='documentacion_subir'),
    path('doc/view/<pk>', MostrarDocumentacion.as_view(), name='documentacion_mostrar'),
    path('doc/list', ListarDocumentacion.as_view(), name='documentacion_listar'),
    #path('doc/upload/success', EntregaCorrecta.as_view(), name='entrega_correcta')
]
