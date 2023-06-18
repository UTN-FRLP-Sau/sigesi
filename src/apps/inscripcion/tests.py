from django.test import TestCase
from .forms import PersonaForm

class PersonaFormTest(TestCase):
    def test_documento_numero_exists(self):
        form_data = {
            'nombre': 'Jorge',
            'apellido': 'RoNCOni',
            'fecha_nacimiento': '15/08/1990',
            'pais_nacimiento': 'Argentina',
            'pais_nacionalidad': '11',
            'documento_tipo': '0',
            'documento_numero': '35299782', #Documento Duplicado
            'domicilio_calle': '123',
            'domicilio_cp': '123',
            'domicilio_numero': '123',
            'telefono': '123',
            'correo_1': 'e@w.com',
            'correo_2': 'e@w.com',
            #'estudiante':
            'escuela': '',
            'especialidad': '5',
            'sexo': '1',
            'genero': ''
        }
        form = PersonaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['documento_numero'], ['El numero de documento ya se encuentra registrado'])

    '''
    def test_documento_numero_does_not_exist(self):
        form_data = {
            'nombre': 'Jorge',
            'apellido': 'RoNCOni',
            'fecha_nacimiento': '15/08/1990',
            'pais_nacimiento': 'Argentina',
            'pais_nacionalidad': '11',
            'documento_tipo': '0',
            'documento_numero': '35299780', #Documento Duplicado
            'domicilio_calle': '123',
            'domicilio_cp': '123',
            'domicilio_numero': '123',
            'telefono': '123',
            'correo_1': 'e@w.com',
            'correo_2': 'e@w.com',
            #'estudiante':
            'escuela': '',
            'especialidad': '5',
            'sexo': '1',
            'genero': ''
        }
        form = PersonaForm(data=form_data)
        self.assertTrue(form.is_valid())
    '''
