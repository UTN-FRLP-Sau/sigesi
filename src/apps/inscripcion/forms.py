from django import forms
import django_bootstrap5.widgets as bw
from django.core.exceptions import ValidationError
from .models import (Pais,
                     TipoDocumento,
                     Escuela,
                     Genero,
                     Persona,
                     ESPECIALIDAD_ESTUDIANTE_CHOICES,
                     SEXO_ESTUDIANTE_CHOICES,
                     MODALIDAD_CHOICES,
                     PERIODO_CHOICES,
                     Documentacion
)

class PersonaForm(forms.Form):
    #persona
    nombre = forms.CharField(max_length=50, label='Nombres')
    apellido = forms.CharField(max_length=50, required=False, label='Apellidos', initial='ronconi')
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', initial='15/08/1990')
    pais_nacimiento = forms.ModelChoiceField(Pais.objects.all(),required=False, label='Pais de nacimiento', initial=11)
    pais_nacionalidad = forms.ChoiceField(choices=[('','---------')]+[(pais.id, pais.nacionalidad.title()) for pais in Pais.objects.all()], initial=11)
    documento_tipo = forms.ModelChoiceField(TipoDocumento.objects.all(),required=False, initial=1)
    documento_numero = forms.CharField(max_length=13,required=False, initial=12)
    domicilio_calle = forms.CharField(max_length=100,required=False, initial=12)
    domicilio_cp = forms.CharField(max_length=100,required=False, initial=12)
    domicilio_numero = forms.IntegerField(required=False, initial=1234)
    telefono = forms.IntegerField(required=False, initial=1234)
    correo_1 = forms.EmailField(initial='e@w.com')
    correo_2 = forms.EmailField(initial='e@w.com')
    #estudiante
    escuela = forms.ModelChoiceField(queryset=Escuela.objects.all(), required=False)
    especialidad = forms.ChoiceField(choices=[('','---------')]+ESPECIALIDAD_ESTUDIANTE_CHOICES, initial=5)
    sexo = forms.ChoiceField(choices=[('','---------')]+SEXO_ESTUDIANTE_CHOICES, initial='m')
    genero = forms.ModelChoiceField(Genero.objects.all(),required=False)

    def clean_documento_numero(self):
        ''' Validacion del Numero de documento

        El metodo valida que el numero de documento no exista en al base de datos, en caso de que no exista
        retorna documento_numero

        Excepciones
        --ValidationError -- Cuando existe el numero devuelve un error
        '''
        documento_numero = self.cleaned_data.get('documento_numero')
        if documento_numero:
            if Persona.objects.filter(numero_documento=documento_numero).exists():
                raise forms.ValidationError('documento_numero', 'El numero de documento ya se encuentra registrado')
        return documento_numero


    '''Validacion de Correo
    def clean_correo_1(self):

        Metodo que valida que ambos correos sean iguiales, y que no exista en la base de datos,
        antes de validar el formulario para que sea enviado retorna el correo_1

        Excepciones:
        -- ValidationError -- Cuando el correo ya existe muestra un error
        -- ValidationError -- Cuando los correos no coinciden muestra un error
        correo_1 = self.cleaned_data.get('correo_1')
        correo_2 = self.cleaned_data.get('correo_2')
        if correo_1==correo_2:
            if Persona.objects.filter(correo=correo_1).exists():
                raise forms.ValidationError('El correo ya se encuentra registrado')
        else:
            raise forms.ValidationError('Los correos no coinciden')
        return correo_1
        '''


    def clean(self):
        # Limpiamos los datos del formulario
        cleaned_data = super(PersonaForm, self).clean()
        # retornamos los datos limpios
        return cleaned_data



class EntregarDocumentacionForm(forms.ModelForm):
    class Meta:
        model = Documentacion
        fields = ['num_documento', 'correo', 'file_documento', 'file_certificado', 'modalidad', 'periodo', 'turno']
        labels = {
            'num_documento': 'Numero de documento o pasaporte',
            'correo': 'Correo electrónico',
            'file_documento': 'Subir identificacion',
            'file_certificado': 'Subir certificado de estudios secundarios',
            'modalidad': 'Elegir modalidad',
            'periodo': 'Elegir periodo',
            'periodo': 'Elegir turno'
        }
