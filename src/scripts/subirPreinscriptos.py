import pandas as pd
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from datetime import datetime
from apps.inscripcion.models import Persona, Estudiante, Genero, Pais, TipoDocumento


# df = pd.read_csv('C:/Users/CIVIL/Desktop/SUI/inscripcion/src/scripts/preinscriptos_todos.csv',
df = pd.read_csv('/home/jronconi/sigesi/src/scripts/preinscriptos_todos.csv',
                 sep=';', header=None, encoding='UTF-8')


def create_email(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context=context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message


def run():
    df_error = pd.DataFrame()
    for i, x in df.iterrows():
        if str(x[11]).lower() == 'm':
            genero = Genero.objects.get(id=7)
        elif str(x[11]).lower() == 'f':
            genero = Genero.objects.get(id=1)
        else:
            genero = Genero.objects.get(id=13)
        if len(str([6]).replace('-', '').replace('_', '')) == 11:
            cuil = str(x[6]).lower()
        else:
            cuil = '11-11111111-1'
        try:
            anio_egreso = int(x[32])
        except:
            anio_egreso = 1900
        pais = Pais.objects.get(nombre=str(x[8]).strip())
        turno = str(x[34])[0].lower()
        carrera = x[33]
        if carrera == 7 or carrera == 27:
            turno = 'n'
        else:
            if turno == 't':
                turno = 'n'

        nueva_fecha = datetime.strptime(
            x[13], "%d/%m/%Y").strftime("%Y-%m-%d")

        persona = Persona(
            apellidos=str(x[1]).lower(),
            nombres=str(x[2]).lower(),
            fecha_nacimiento=nueva_fecha,
            sexo=str(x[11]).lower(),
            genero=genero,
            pais_nacimiento=pais,
            nacionalidad=pais,
            documento_tipo=TipoDocumento.objects.get(id=1),
            numero_documento=str(x[5]).lower(),
            cuil=cuil,
            pais_documento=pais,
            domicilio_pais=pais,
            telefono=str(x[24]),
            correo=str(x[12]).lower()
        )
        try:
            persona.save()
        except:
            df_error = pd.concat([df_error, df.loc[i:i]])
        else:
            estudiante = Estudiante(
                legajo=0,
                anio_egreso=anio_egreso,
                titulo_secundario='tituloescuela',
                emergencia_telefono='',
                emergencia_contacto='',
                especialidad=x[33],
                turno=turno,
                modalidad='p',
                persona=persona
            )
            try:
                estudiante.save()
            except:
                df_error = pd.concat([df_error, df.loc[i:i]])
            else:
                email = create_email(
                    user_mail=persona.correo,
                    subject='Confirmación de Inscripción',
                    template_name='inscripcion/confirmacion_correo_1.html',
                    context={
                        'nombre': persona.nombres.title(),
                        'apellido': persona.apellidos.upper(),
                        'carrera': estudiante.get_especialidad_display(),
                        'turno': estudiante.get_turno_display(),
                        'modalidad': estudiante.get_modalidad_display(),
                        'url': 'https://ingreso.frlp.utn.edu.ar/inscripcion/verificar-dni/{}/'.format(estudiante.pk)
                    }
                )
                email.send()

    df_error.to_csv(
        '/home/jronconi/sigesi/src/scripts/errores.csv')


run()
