# from typing import Any, Dict
# from collections.abc import Mapping
# from typing import Any
from typing import Any
from django import forms
# import django_bootstrap5.widgets as bw
from django.core.exceptions import ValidationError
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from .models import (Pais,
                     Provincia,
                     PartidoPBA,
                     Localidad,
                     Estudiante,
                     Persona,
                     Archivos,
                     Escuela,
                     ESPECIALIDAD_ESTUDIANTE_CHOICES,
                     TURNO_INGRESO_CHOICES,
                     SEXO_ESTUDIANTE_CHOICES,
                     Documentacion
                     )


def validar_cuil(dni, cuil, *args, **kwargs):
    # Verificar longitud del CUIL
    if len(cuil) != 11:
        return (False, 1)
    # Verificar que los primeros dos dígitos sean numéricos
    if not cuil[:2].isdigit():
        return (False, 2)
    # Verificar que el último dígito sea numérico
    if not cuil[-1].isdigit():
        return (False, 3)
    # Verificar que los 8 dígitos centrales sean el número de documento
    if not cuil[2:10].isdigit():
        return (False, 4)
    if cuil[2:10] != dni:
        print(cuil[2:10])
        print(dni)
        return (False, 5)
    return (True, 0)


'''
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
            'modalidad': 'La modalidad Semi-Presencial solo es para las personas que no residan en La Plata, Berisso y Ensenada',
        }

'''


class NacionalidadModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nacionalidad


class CreatePersonaForm(forms.ModelForm):
    correo2 = forms.EmailField(max_length=255, label='Confirmar Correo')
    telefono2 = forms.IntegerField(label='Confirmar Telefono')
    nacionalidad = NacionalidadModelChoiceField(queryset=Pais.objects.all())
    domicilio_provincia = forms.ModelChoiceField(queryset=Provincia.objects.none(),
                                                 label='Provincia',
                                                 required=False
                                                 )
    domicilio_partido = forms.ModelChoiceField(queryset=PartidoPBA.objects.none(),
                                               label='Partido',
                                               required=False,
                                               )
    domicilio_localidad = forms.ModelChoiceField(queryset=Localidad.objects.none(),
                                                 label='Localidad',
                                                 required=False,
                                                 )

    class Meta:
        model = Persona
        fields = ['apellidos',
                  'nombres',
                  'nombre_autopercibido',
                  'sexo',
                  'genero',
                  'genero_otro',
                  'fecha_nacimiento',
                  'pais_nacimiento',
                  'nacionalidad',
                  'documento_tipo',
                  'numero_documento',
                  'cuil',
                  'telefono',
                  'telefono2',
                  'correo',
                  'correo2',
                  'pais_documento',
                  'domicilio_pais',
                  'domicilio_provincia',
                  'domicilio_partido',
                  'domicilio_localidad',
                  'domicilio_barrio',
                  'domicilio_calle',
                  'domicilio_altura',
                  'domicilio_piso',
                  'domicilio_departamento',
                  # 'domicilio_cpa',
                  # 'domicilio_cp4',
                  # 'domicilio_coordenada_x',
                  # 'domicilio_coordenada_y',
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
            # 'domicilio_cpa': 'CPA',
            # 'domicilio_cp4': 'CP4',
            'telefono': 'Numero de telefono',
            'correo': 'Correo electronico'
        }
        help_texts = {
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(CreatePersonaForm, self).__init__(*args, **kwargs)
        self.fields['domicilio_provincia'].queryset = Provincia.objects.none()
        self.fields['domicilio_partido'].queryset = PartidoPBA.objects.none()
        self.fields['domicilio_localidad'].queryset = Localidad.objects.none()

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(
                self.error_messages["Selección no válida"], code='invalid_choice')
        return value

    def clean(self):
        # Limpiamos los datos del formulariodef clean(self):
        cleaned_data = super().clean()

        # Eliminamos puntos y guiones del DNI
        dni = cleaned_data.get("numero_documento")
        if dni:
            cleaned_data['numero_documento'] = dni.replace(
                ".", "").replace("-", "").replace(",", "")

        # Verificamos el CUIL
        cuil = cleaned_data.get("cuil")
        dni = cleaned_data.get("numero_documento")
        if cuil:
            # Eliminar guiones del CUIL y del DNI
            cuil = cuil.replace("-", "").replace(".", "").replace(",", "")
            dni = dni.replace("-", "").replace(".", "").replace(",", "")
            cuil_valid = validar_cuil(dni, cuil)
            if not cuil_valid[0]:
                if cuil_valid[1] == 1:
                    self.add_error(
                        'cuil', "El CUIL debe tener una longitud de 11 caracteres.")
                if cuil_valid[1] == 2:
                    self.add_error(
                        'cuil', "En el CUIL, los 2 primeros caracteres deben ser un número")
                if cuil_valid[1] == 3:
                    self.add_error(
                        'cuil', "En el CUIL, el ultimo caracter debe ser un número")
                if cuil_valid[1] == 4:
                    self.add_error(
                        'cuil', "En el CUIL, los 8 caracteres centrales deben ser un número")
                if cuil_valid[1] == 5:
                    self.add_error(
                        'cuil', "En el CUIL, no contiene el número de DNI")

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
        # retornamos la info limpia
        return cleaned_data


class CreateStudentForm(forms.ModelForm):
    pais = forms.ModelChoiceField(queryset=Pais.objects,
                                  label='Pais donde curso el secundario',
                                  required=False
                                  )
    provincia = forms.ModelChoiceField(queryset=Provincia.objects,
                                       label='Provincia donde curso el secundario',
                                       required=False
                                       )
    partido = forms.ModelChoiceField(queryset=PartidoPBA.objects,
                                     label='Partido donde curso el secundario',
                                     required=False,
                                     )
    localidad = forms.ModelChoiceField(queryset=Localidad.objects,
                                       label='Localidad donde curso el secundario',
                                       required=False,
                                       )

    class Meta:
        model = Estudiante
        fields = [  # 'credencial',
            # 'legajo',
            'pais',
            'provincia',
            'partido',
            'localidad',
            'escuela',
            'anio_egreso',
            'titulo_secundario',
            'emergencia_telefono',
            'emergencia_contacto',
            'especialidad',
            'turno',
            'modalidad',
            # 'persona'
        ] 
        labels = {
            'escuela': 'Escuela',
            'anio_egreso': 'En que año egresaste del secundario',
            'titulo_secundario': 'Cual es el titulo con el que egresaste',
            'emergencia_contacto': 'Nombre del Contacto de Emergencia',
            'emergencia_telefono': 'Telefono de Emergencia',
            'especialidad': 'Carrera',
            'turno': 'Turno',
            'modalidad': 'Modalidad'
        }
        help_texts = {
        }


    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        self.fields['pais'].queryset = Pais.objects
        self.fields['provincia'].queryset = Provincia.objects
        self.fields['partido'].queryset = PartidoPBA.objects
        self.fields['localidad'].queryset = Localidad.objects
        self.fields['escuela'].queryset = Escuela.objects

    def clean(self):
        # Limpiamos los datos del formulariodef clean(self):
        cleaned_data = super().clean()
        # retornamos la info limpia
        return cleaned_data



class VerificacionInscripcionForm(forms.Form):
    dni = forms.CharField(max_length=16, label='Numero de Documento')


class ActualizarInscripcionForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['especialidad',
                  'turno',
                  'modalidad',
                  ]
        labels = {'especialidad': 'Carrera',
                  'turno': 'Turno',
                  'modalidad': 'Modalidad'
                  }
        help_texts = {}


class SubirDocumentoForm(forms.ModelForm):
    class Meta:
        model = Archivos
        fields = ['path',]
        labels = {'path': 'PDF1: Identificación, Documento o Pasaporte'}
        help_texts = {'path': 'Solo se acepta formato PDF'}


class SubirCertificadoForm(forms.ModelForm):
    class Meta:
        model = Archivos
        fields = ['path',]
        labels = {'path': 'PDF2: Certificado de Estudios Secundarios'}
        help_texts = {'path': 'Solo se acepta formato PDF'}
