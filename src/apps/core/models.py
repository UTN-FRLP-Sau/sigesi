from django.db import models
import os
from uuid import uuid4

# Create your models here.


def _generar_ruta_file_documento(instance, filename):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Validacion y normalizacion de la ruta
    ruta_validada = 'landing'
    # Generamos el nombre del archivo con un idenfiticar aleatorio y la extension del archivo original
    nombre_archivo = '{}.{}'.format(uuid4().hex, extension)
    # Retornamos la ruta completa
    return os.path.join(ruta_validada, nombre_archivo)


class ConfigLandingPage(models.Model):
    inscripcion_masinfo = models.FileField(
        upload_to=_generar_ruta_file_documento)

    class Meta:
        verbose_name = "Landing Page Configuración"
        verbose_name_plural = "Landing Page Configuraciones"

    def __str__(self):
        return "Configuración Landing Page"

    def save(self, *args, **kwargs):
        self.pk = 1  # fuerza siempre el mismo ID
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # opcional: evitar que se borre
