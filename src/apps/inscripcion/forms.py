#from typing import Any, Dict
from collections.abc import Mapping
from typing import Any
from django import forms
#import django_bootstrap5.widgets as bw
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
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
    domicilio_pais = forms.ModelChoiceField(queryset=Pais.objects.all(),
                                            label='Pais',
                                            #required=True,
                                            #widget=forms.Select(
                                            #    attrs={
                                            #        'onchange': 'show_provincia();',
                                            #        }
                                            #    )
                                            )
    domicilio_provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(),
                                                 label='Provincia',
                                                 #required=True,
                                                 #widget=forms.Select(
                                                 #    attrs={
                                                 #        'onchange': 'show_partido();',
                                                 #        }
                                                 #    )
                                                 )
    domicilio_partido = forms.ModelChoiceField(queryset=PartidoPBA.objects.all(),
                                               label='Partido',
                                               #required=True,
                                               #widget=forms.Select(
                                               #     attrs={
                                               #         'onchange': 'show_localidad();',
                                               #          }
                                               #     )
                                                )
    domicilio_localidad = forms.ModelChoiceField(queryset=Localidad.objects.all(),
                                               label='Localidad',
                                               #required=True,
                                               #widget=forms.Select(
                                               #     attrs={
                                               #         'onchange': 'show_localidad();',
                                               #          }
                                               #     )
                                                )


    class Meta:
        model = Persona
        fields = ['apellidos',#
                  'nombres',#
                  'fecha_nacimiento',#
                  'pais_nacimiento',#
                  'nacionalidad',#
                  'documento_tipo',#
                  'numero_documento',#
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
                  'domicilio_piso',
                  'domicilio_departamento',
                  #'domicilio_cpa',
                  #'domicilio_cp4',
                  # 'domicilio_coordenada_x',
                  # 'domicilio_coordenada_y',
                  ]
        labels = {
            'apellido': 'Apellidos',
            'nombre': 'Nombres',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'pais_nacimiento': 'Pais de nacimiento',
#            'nacionalidad': 'Nacionalidad',
            'documento_tipo': 'Tipo de documento',
            'numero_documento': 'Numero de documento, o codigo de credencial',
            'pais_documento': 'Pais de origen del documento',
            'domicilio_pais': 'Pais',
            'domicilio_provincia': 'Provincia',
            'domicilio_partido': 'Partido',
            'domicilio_localidad': 'Localidad',
            'domicilio_barrio': 'Barrio',
            'domicilio_calle': 'Calle',
            'domicilio_piso': 'Piso',
            'domicilio_departamento': 'Departamento',
            #'domicilio_cpa': 'CPA',
            #'domicilio_cp4': 'CP4',
            'telefono': 'Numero de telefono',
            'correo': 'Correo electronico'
        }
        help_texts ={
            'apellido': 'Tal como aparece en su documento',
            'nombre': 'Tal como aparece en su documento',
            'telefono': 'Sin 0 ni 15, ejemplo 3446565656',
        }
        widgets ={
            #'domicilio_localidad': forms.Select(attrs={ 'data-live-search':'true'}),
            #'domicilio_barrio': forms.TextInput(attrs={'style':'display:none'}),
            #'domicilio_calle': forms.TextInput(attrs={'style':'display:none'}),
            #'domicilio_piso': forms.TextInput(attrs={'style':'display:none'}),
            #'domicilio_departamento': forms.TextInput(attrs={'style':'display:none'}),
#            'nacionalidad': NacionalidadModelChoiceField(queryset=Pais.objects.all())
#            'nacionalidad': forms.Select(choices=Pais.objects.values_list('nacionalidad', 'nacionalidad'))
        }

    def __init__(self, *args, **kwargs):
        super(CreatePersonaForm, self).__init__(*args, **kwargs)
        self.fields['domicilio_provincia'].queryset = Provincia.objects.none()
        self.fields['domicilio_partido'].queryset = PartidoPBA.objects.none()
        self.fields['domicilio_localidad'].queryset = Localidad.objects.none()


class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [#'legajo',
                  'cuil', 'sexo', 'genero', 'nombre_autopercibido', 'escuela', 'anio_egreso', 'titulo_secundario',
            'emergencia_telefono', 'emergencia_contacto', 'especialidad', 'turno', 'modalidad']#, 'persona']
        labels = {
            'cuil': 'Cuil/Cuit',
            'sexo': 'Sexo',
            'genero': 'Genero',
            'nombre_autopercibido': 'Como preferis que te llamen',
            'escuela':'Escuela',
            'anio_egreso': 'En que año egresaste del secundario',
            'titulo_secundario': 'Cual es el titulo con el que egresaste',
            'emergencia_contacto': 'Nombre del Contacto de Emergencia',
            'emergencia_telefono': 'Telefono de Emergencia',
            'especialidad': 'Carrera',
            'turno': 'Turno de Preferencia',
            'modalidad': 'Modealidad de cursado'
            }
        help_texts ={

        }
