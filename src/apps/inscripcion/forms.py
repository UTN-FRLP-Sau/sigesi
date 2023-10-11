#from typing import Any, Dict
#from collections.abc import Mapping
#from typing import Any
from typing import Any
from django import forms
#import django_bootstrap5.widgets as bw
from django.core.exceptions import ValidationError
#from django.core.files.base import File
#from django.db.models.base import Model
#from django.forms.utils import ErrorList
from .models import (Pais,
                     Provincia,
                     PartidoPBA,
                     Localidad,
                     Estudiante,
                     Persona,
                     ESPECIALIDAD_ESTUDIANTE_CHOICES,
                     TURNO_INGRESO_CHOICES,
                     SEXO_ESTUDIANTE_CHOICES,
                     Documentacion
)


class EntregarDocumentacionForm(forms.ModelForm):
    class Meta:
        model = Documentacion
        fields = ['num_documento', 'correo', 'file_documento', 'file_certificado', 'periodo', 'modalidad', 'turno']
        labels = {
            'num_documento': 'Numero de documento o pasaporte',
            'correo': 'Correo electrónico',
            'file_documento': 'Subir identificacion',
            'file_certificado': 'Subir certificado de estudios secundarios',
            'periodo': '¿Cuándo quiero cursar?',
            'modalidad': '¿Cómo lo quiero cursar?',
            'turno': '¿En qué turno quiero cursar?'
        }
        help_texts ={
            'modalidad': 'La modalidad Semi-Presencial solo es para las personas que no residan en La Plata, Berisso o Ensenada',
        }


class NacionalidadModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nacionalidad


class CreatePersonaForm(forms.ModelForm):
    correo2 = forms.EmailField(max_length=255, label='Confirmar Correo')
    telefono2 = forms.IntegerField(label='Confirmar Telefono')
    nacionalidad = NacionalidadModelChoiceField(queryset=Pais.objects.all())
    domicilio_provincia = forms.ModelChoiceField(queryset=Provincia.objects,
                                                 label='Provincia',
                                                 required=False
                                                 )
    domicilio_partido = forms.ModelChoiceField(queryset=PartidoPBA.objects,
                                               label='Partido',
                                               required=False,
                                                )
    domicilio_localidad = forms.ModelChoiceField(queryset=Localidad.objects,
                                               label='Localidad',
                                               required=False,
                                                )

    class Meta:
        model = Persona
        fields = ['apellidos',#
                  'nombres',#
                  'nombre_autopercibido',
                  'sexo',
                  'genero',
                  'genero_otro',
                  'fecha_nacimiento',#
                  'pais_nacimiento',#
                  'nacionalidad',#
                  'documento_tipo',#
                  'numero_documento',#
                  'cuil',
                  'telefono',
                  'telefono2',
                  'correo',
                  'correo2',
                  'pais_documento',#
                  'domicilio_pais',
                  'domicilio_provincia',
                  'domicilio_partido',
                  'domicilio_localidad',
                  'domicilio_barrio',
                  'domicilio_calle',
                  'domicilio_altura',
                  'domicilio_piso',
                  'domicilio_departamento',
                  #'domicilio_cpa',
                  #'domicilio_cp4',
                  #'domicilio_coordenada_x',
                  #'domicilio_coordenada_y',
                  ]
        labels = {
            'apellido': 'Apellidos',
            'nombre': 'Nombres',
            'nombre_autopercibido': 'Como preferis que te llamen',
            'sexo': 'Sexo',
            'genero': 'Genero',
            'genero_otro': 'Des. Genero',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'pais_nacimiento': 'Pais de nacimiento',
            'nacionalidad': 'Nacionalidad',
            'documento_tipo': 'Tipo de documento',
            'numero_documento': 'Numero de documento, o codigo de credencial',
            'cuil': 'CUIT/CUIL',
            'pais_documento': 'Pais de origen del documento',
            'domicilio_pais': 'Pais',
            'domicilio_provincia': 'Provincia',
            'domicilio_partido': 'Partido',
            'domicilio_localidad': 'Localidad',
            'domicilio_barrio': 'Barrio',
            'domicilio_calle': 'Calle',
            'domicilio_altura': 'Altura o Numero de Puerta',
            'domicilio_piso': 'Piso',
            'domicilio_departamento': 'Departamento',
            #'domicilio_cpa': 'CPA',
            #'domicilio_cp4': 'CP4',
            'telefono': 'Numero de telefono',
            'correo': 'Correo electronico'
        }
        help_texts ={
        }
        widgets ={
        }

    def __init__(self, *args, **kwargs):
        super(CreatePersonaForm, self).__init__(*args, **kwargs)
        self.fields['domicilio_provincia'].queryset = Provincia.objects
        self.fields['domicilio_partido'].queryset = PartidoPBA.objects
        self.fields['domicilio_localidad'].queryset = Localidad.objects

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(self.error_messages["Selección no válida"], code='invalid_choice')
        return value

    def clean(self):
        # Limpiamos los datos del formulariodef clean(self):
        cleaned_data = super().clean()
        # Comparamos los telefonos:
        telefono = cleaned_data.get("telefono")
        telefono2 = str(cleaned_data.get("telefono2"))
        if telefono and telefono2 and telefono != telefono2:
            self.add_error('telefono2', "Los numeros telefonicos no coinciden")
        # Comparamos los correos:
        correo = cleaned_data.get("correo")
        correo2 = cleaned_data.get("correo2")
        if correo and correo2 and correo != correo2:
            self.add_error('correo2', "Los correos no coinciden")
        #retornamos la info limpia
        return cleaned_data


class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [#'credencial',
                  #'legajo',
                  'escuela',
                  'anio_egreso',
                  'titulo_secundario',
                  'emergencia_telefono',
                  'emergencia_contacto',
                  'especialidad',
                  'turno',
                  'modalidad',
                  #'persona'
                  ]
        labels = {
            'escuela':'Escuela',
            'anio_egreso': 'En que año egresaste del secundario',
            'titulo_secundario': 'Cual es el titulo con el que egresaste',
            'emergencia_contacto': 'Nombre del Contacto de Emergencia',
            'emergencia_telefono': 'Telefono de Emergencia',
            'especialidad': 'Carrera',
            'turno': 'Turno',
            'modalidad': 'Modealidad'
            }
        help_texts ={

        }


class VerificacionInscripcionForm(forms.Form):
    dni = forms.CharField(max_length=16, label='Numero de Documento')
