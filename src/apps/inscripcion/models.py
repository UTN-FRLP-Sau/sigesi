# future
# Librerias Standars
import os
from uuid import uuid4
from datetime import date
import re
# Librerias de Terceros
# Django
from django.db import models
# Django Locales


# Create your models here.

GESTION_ESCUELA_CHOICES = [("privada", "Privada"),
                           ("publica", "Publica"),
                           ("mixta", "Mixta"),
                           ("social/cooperativa", "Social/Cooperativa")]

AMBITO_ESCUELA_CHOICES = [
    ("rural", "Rural"),
    ("urbano", "Urbano")
]

SEXO_ESTUDIANTE_CHOICE = [
    ("m", "Masculino"),
    ("f", "Femenino")
]

ESPECIALIDAD_ESTUDIANTE_CHOICE = [
    (5, "Ing. en Sistemas de Informacion"),
    (7, "Ing. en Energia Electrica"),
    (17, "Ing. Mecanica"),
    (24, "Ing. Industrial"),
    (27, "Ing. Quimica"),
    (31, "Ing. Civil")
]


TURNO_ESTUDIANTE_CHOICES = [
    ("m", "Turno Mañana"),
    ("t", "Turno Tarde"),
    ("n", "Turno Noche")
]


def _generar_ruta_documento(instance, filename):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Generamos la ruta relativa a media_root
    # # donde almacenar el archivo usando la fecha actual
    # año/mes/dia
    ruta = os.path.join('static/media/documentos', date.today().strftime('%y/%m/%d'))
    # Generamos el nombre del archivo con un idenfiticar
    # aleatorio y la extension del archivo original
    nombre_archivo = '{}.{}'.format(uuid4().hex,extension)
    # Retornamos la ruta completa
    return os.path.join(ruta, nombre_archivo)


class PartidoPBA(models.Model):
    id = models.CharField(max_length=5,
                          primary_key=True,
                          unique=True,
                          db_column='id')
    nombre = models.CharField(max_length=100, db_column='nombre', unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        db_table = 'partidopba'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre = self.nombre.lower()
        super(PartidoPBA, self).save()
        
    def get_absolute_url():
        pass


class Pais(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', unique=True)
    nombre = models.CharField(max_length=50, db_column='nombre', unique=True)
    coord_x = models.FloatField(db_column='coordenadaX')
    coord_y = models.FloatField(db_column='coordenadaY')
    nacionalidad = models.CharField(
        max_length=100, db_column='nacionalidad', unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'pais'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre=self.nombre.lower()
        self.nacionalidad = self.nacionalidad.lower()
        super(Pais, self).save()

    def get_absolute_url():
        pass

class Provincia(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', unique=True)
    nombre = models.CharField(max_length=50, db_column='nombre', unique=True)
    pais = models.ForeignKey(Pais,
                             on_delete=models.DO_NOTHING,
                             db_column='pais')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        db_table = 'provincia'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre=self.nombre.lower()
        super(Provincia, self).save()

    def get_absolute_url():
        pass

class Localidad(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', unique=True)
    nombre = models.CharField(max_length=51, db_column='nombre')
    partido = models.ForeignKey(PartidoPBA,
                                on_delete=models.DO_NOTHING,
                                null=True,
                                blank=True,
                                db_column='Partido')
    provincia = models.ForeignKey(Provincia,
                                  on_delete=models.DO_NOTHING,
                                  db_column='provincia')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        db_table = 'localidad'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre=self.nombre.lower()
        super(Localidad,self).save()

    def get_absolute_url():
        pass

class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=50, db_column='tipo', unique=True)

    class Meta:
        ordering=['tipo']
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        db_table = 'tipodocumento'

    def __str__(self):
        return '{}'.format(self.tipo.title())

    def save(self):
        self.tipo = self.tipo.lower()
        super(TipoDocumento,self).save()

    def get_absolute_url():
        pass
class Persona(models.Model):
    apellidos = models.CharField(max_length=60, db_column='apellidos')
    nombres = models.CharField(max_length=60, db_column='nombres')
    fecha_nacimiento = models.DateField(db_column='nacimientofecha')
    pais_nacimiento = models.ForeignKey(Pais,
                                        on_delete=models.DO_NOTHING,
                                        related_name='pais_nacimiento',
                                        db_column='nacimientopais')
    nacionalidad = models.ForeignKey(Pais,
                                     on_delete=models.DO_NOTHING,
                                     related_name='pais_nacionalidad',
                                     db_column='nacionalidad')
    documento_tipo = models.ForeignKey(TipoDocumento,
                                       on_delete=models.DO_NOTHING,
                                       db_column='documentotipo')
    numero_documento = models.CharField(max_length=16, db_column='documentonumero', unique=True)
    pais_documento = models.ForeignKey(Pais,
                                       on_delete=models.DO_NOTHING,
                                       related_name='pais_documento_emisor',
                                       db_column='documentopaisemisor')
    domicilio_piso = models.CharField(max_length=4,
                                      default=None,
                                      null=True,
                                      blank=True,
                                      db_column='domiciliopiso')
    domicilio_departamento = models.CharField(max_length=4,
                                      default=None,
                                      null=True,
                                      blank=True,
                                      db_column='domiciliodepartamento')
    domicilio_barrio = models.CharField(max_length=30,
                                      default=None,
                                      null=True,
                                      blank=True,
                                      db_column='domiciliobarrio')
    domicilio_localidad = models.ForeignKey(Localidad,
                                            on_delete=models.DO_NOTHING,
                                            db_column='domiciliolocalidad')
    domicilio_cpa = models.CharField(max_length=8, db_column='domicilioCPA')
    domicilio_cp4 = models.CharField(max_length=4, db_column='domicilioCP4')
    domicilio_coordenada_x = models.FloatField(db_column='domiciliocoordenadaX')
    domicilio_coordenada_y = models.FloatField(db_column='domiciliocoordenadaY')
    telefono = models.CharField(max_length=20, db_column='telefono')
    correo = models.EmailField(max_length=254, db_column='email', unique=True)

    class Meta:
        ordering = ['apellidos']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'persona'

    def __str__(self):  # Python 3
        return '{}, {}'.format(self.apellidos.upper(), self.nombres.title())

    def save(self):
        self.apellidos=self.apellidos.lower()
        self.nombres = self.nombres.lower()
        self.numero_documento = self.numero_documento.lower()
        self.domicilio_piso = self.domicilio_piso.lower()
        self.domicilio_departamento = self.domicilio_departamento.lower()
        self.domicilio_localidad = self.domicilio_localidad.lower()
        self.domicilio_barrio = self.domicilio_barrio.lower()
        self.domicilio_cpa = self.domicilio_cpa.lower()
        self.domicilio_cp4 = self.domicilio_cp4.lower()
        self.telefono =self.telefono.lower()
        self.correo = self.correo.lower()
        super(Persona, self).save()
        
    def get_absolute_url():
        pass


class Escuela(models.Model):
    cue = models.CharField(max_length=9,
                           primary_key=True,
                           unique=True,
                           db_column='CUE')
    gestion = models.CharField(max_length=20,
                               choices=GESTION_ESCUELA_CHOICES,
                               db_column='gestion')
    ambito = models.CharField(max_length=20,
                              choices=AMBITO_ESCUELA_CHOICES,
                              db_column='ambito')
    tecnica = models.BooleanField(db_column='tecnica')
    nombre = models.CharField(max_length=150,
                              db_column='nombre')
    domicilio_calle = models.CharField(max_length=150,
                                       db_column='domiciliocalle')
    domicilio_altura = models.IntegerField(db_column='domicilioaltura')
    domicilio_localidad = models.ForeignKey(Localidad,
                                            on_delete=models.DO_NOTHING,
                                            db_column='domiciliolocalidad')
    domicilio_cpa = models.CharField(max_length=8, db_column='domicilioCPA')
    domicilio_cp4 = models.CharField(max_length=4, db_column='domicilioCP4')
    domicilio_coordenada_x = models.FloatField(default=0, db_column='domiciliocoordenadaX')
    domicilio_coordenada_y = models.FloatField(default=0, db_column='domiciliocoordenadaY')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Escuela'
        verbose_name_plural = 'Escuelas'
        db_table = 'escuela'

    def __str__(self):  # Python 3
        return '{} ({})'.format(self.nombre.title(), self.cue)

    def save(self):
        self.gestion = self.gestion.lower()
        self.ambito = self.ambito.lower()
        self.nombre = self.nombre.lower()
        self.domicilio_calle = self.domicilio_calle.lower()
        self.domicilio_cpa = self.domicilio_cpa.lower()
        self.domicilio_cp4 = self.domicilio_cp4.lower()
        super(Escuela, self).save()

    def get_absolute_url():
        pass

class TelefonoEscuela(models.Model):
    telefono = models.CharField(max_length=50, db_column='telefono')
    escuela = models.ForeignKey(Escuela,
                            on_delete=models.DO_NOTHING,
                            db_column='escuela')

    class Meta:
        ordering = ['escuela']
        verbose_name = 'Telefono de la Escuela'
        verbose_name_plural = 'Telefonos de las Escuelas'
        db_table = 'telefonoEscuela'

    def __str__(self):  # Python 3
        return '{}-{}'.format(self.escuela.nombre, self.telefono)

    def save(self):
        self.telefono = self.telefono.lower()
        super(TelefonoEscuela, self).save()
        
    def get_absolute_url():
        pass


class MailEscuela(models.Model):
    escuela = models.ForeignKey(Escuela,
                            max_length=9,
                            on_delete=models.DO_NOTHING,
                            db_column='escuela')
    mail = models.EmailField(max_length=254, db_column='mail')

    class Meta:
        ordering = ['escuela']
        verbose_name = 'Correo Electronico de la Escuela'
        verbose_name_plural = 'Correos Electronicos de las Escuelas'
        db_table = 'mailescuela'

    def __str__(self):  # Python 3
        return '{}-{}'.format(self.escuela.nombre, self.mail)

    def save(self):
        self.mail=self.mail.lower()
        super(MailEscuela, self).save()
        
    def get_absolute_url():
        pass


class Genero(models.Model):
    nombre = models.CharField(db_column='nombre', max_length=45, unique=True)

    class Meta:
        ordering=['nombre']
        db_table = 'genero'
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

    def __str__(self):
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre = self.nombre.lower()
        super(Genero, self).save()

    def get_absolute_url():
        pass


class Docente(models.Model):
    cbu = models.IntegerField(db_column='cbu', unique=True)
#    comprobante = models.FileField(db_column='comprobante', upload_to=_generar_ruta_documento)
    genero = models.ForeignKey(Genero, on_delete=models.DO_NOTHING, db_column='genero')
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        ordering=['persona']
        db_table = 'docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return '{}, {}'.format(self.persona.apellidos.upper(), self.persona.nombres.title())

    def save(self):
        super(Docente, self).save()

    def get_absolute_url():
        pass


class TituloSecundario(models.Model):
    titulo = models.CharField(max_length=45, db_column='titulo', unique=True)
    tecnico = models.BooleanField(db_column='tecnico')

    class Meta:
        ordering=['titulo']
        db_table = 'tituloescuela'
        verbose_name = 'Titulo'
        verbose_name_plural = 'Titulos'

    def __str__(self):
        return '{}'.format(self.titulo.title())

    def save(self):
        self.titulo = self.titulo.lower()
        super(TituloSecundario, self).save()

    def get_absolute_url():
        pass


class Estudiante(models.Model):
    credencial = models.IntegerField(primary_key=True,
                                     db_column='credencial',
                                     unique=True,
                                     auto_created=True)
    legajo = models.IntegerField(default=0, db_column='legajo', unique=True)
    cuil = models.CharField(max_length=13, null=True, blank=True, db_column='cuil')
    sexo = models.CharField(max_length=1, db_column='sexo', choices=SEXO_ESTUDIANTE_CHOICE, null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.DO_NOTHING, db_column='genero', null=True, blank=True)
    nombre_autopercibido = models.CharField(max_length=60, db_column='nombreautopercibido', null=True, blank=True)
    escuela = models.ForeignKey(Escuela, on_delete=models.DO_NOTHING, db_column='escuela', null=True, blank=True)
    anio_egreso = models.IntegerField(null=True, blank=True, db_column='escuelaanioegreso')
    titulo_secundario = models.ForeignKey(TituloSecundario, db_column='tituloescuela', null=True, blank=True, on_delete=models.DO_NOTHING)
    emergencia_telefono = models.CharField(max_length=20, db_column='emergenciatelefono', null=True, blank=True)
    emergencia_contacto = models.CharField(max_length=60, db_column='emergenciacontacto', null=True, blank=True)
    especialidad = models.IntegerField(choices=ESPECIALIDAD_ESTUDIANTE_CHOICE, db_column='especialidad', null=True, blank=True)
    turno = models.CharField(max_length=1, null=True, blank=True, db_column='turno', choices=TURNO_ESTUDIANTE_CHOICES)
    modalidad =models.IntegerField(db_column='modalidad', null=True, blank=True)
    persona = models.OneToOneField(Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        ordering=['credencial']
        db_table = 'estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantess'

    def __str__(self):
        return '{}, {}'.format(self.persona.apellidos.upper(), self.persona.nombres.title())

    def save(self):
        #Guardamos todo en minusculas
        self.nombre_autopercibido = self.nombre_autopercibido.lower()
        self.titulo_secundario = self.titulo_secundario.lower()
        self.emergencia_contacto = self.emergencia_contacto.lower()
        
        #Damos el formato de cuil de la forma XX-XXXXXXXX-X
        patron = r'^\d{2}-\d{8}-\d$'
        cuil = self.cuil
        cuil = cuil.replace("-","")
        if re.match(patron, cuil):
            self.cuil = cuil[:2]+'-'+cuil[2:11]+'-'+cuil[11:]
        super(Estudiante, self).save()
        
    def get_absolute_url():
        pass


class Archivos(models.Model):
    tipo = models.IntegerField(db_column='tipo')
    path = models.FileField(db_column='ubicacion', upload_to=_generar_ruta_documento)
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        db_table = 'imagenes'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivoss'

    def __str__(self):
        return '({}) - {}, {}'.format(self.id, self.persona.apellidos.upper(), self.persona.nombres.title())
    
    def save(self):
        super(Archivos, self).save()
        
    def get_absolute_url():
        pass


class Aula(models.Model):
    nombre = models.CharField(db_column='denominacion', max_length=20, unique=True)
    capacidad = models.IntegerField(db_column='capacidad')
    aire = models.BooleanField(db_column='aire')
    proyector = models.BooleanField(db_column='proyector')
    accesibilidad = models.BooleanField(db_column='accesibiliad')

    class Meta:
        ordering=['nombre']
        db_table = 'aula'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre = self.nombre.lower()
        super(Aula, self).save()

    def get_absolute_url():
        pass


class ModalidadCursado(models.Model):
    nombre = models.CharField(max_length=15, db_column='nombre', unique=True)
    descripcion = models.CharField(max_length=150, db_column='descripcion')

    class Meta:
        db_table = 'modalidadcursada'
        verbose_name = 'Modalidad'
        verbose_name_plural = 'Modalidades'

    def __str__(self):
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre = self.nombre.lower()
        self.descripcion = self.descripcion.lower()

    def get_absolute_url():
        pass


class Comision(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING, db_column='aula')
    nombre = models.CharField(max_length=4, db_column='nombre')
    modalidad = models.ForeignKey(ModalidadCursado, on_delete=models.DO_NOTHING, db_column='modalidadcursada')
    ingreso_anio = models.IntegerField(db_column='ingresoanio')
    estudiante = models.ManyToManyField(Estudiante, db_table='matricula')

    class Meta:
        unique_together = ['nombre', 'ingreso_anio']
        ordering = ['ingreso_anio','nombre']
        db_table = 'comision'
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'

    def __str__(self):
        return '{}-{}'.format(self.nombre.upper(), self.ingreso_anio)

    def save(self):
        self.nombre = self.nombre.lower()
        super(Comision, self).save()

    def get_absolute_url():
        pass


class EquipoDocente(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision')
    docente = models.ForeignKey(Docente, on_delete=models.DO_NOTHING, db_column='docente')
    profesor = models.BooleanField(db_column='profesor')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comision', 'docente'],
                name='unique_combination_comision_docente'
                )]
        db_table = 'equipodocente'
        verbose_name = 'Equipo Docente'
        verbose_name_plural = 'Equipos Docentes'

    def __str__(self):
        return '{}-{}'.format(self.comision.nombre.upper(), self.docente.persona.apellidos.upper())
    
    def save(self):
        super(EquipoDocente, self).save()

    def get_absolute_url():
        pass


class Unidad(models.Model):
    nombre = models.CharField(max_length=45, db_column='nombre', unique=True)
    detalle = models.CharField(max_length=100, db_column='detalle')

    class Meta:
        db_table = 'unidad'
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre=self.nombre.lower()
        self.detalle=self.detalle.lower()
        super(Unidad, self).save()

    def get_absolute_url():
        pass



class Clase(models.Model):
    nombre = models.CharField(max_length=45, db_column='nombre', unique=True)
    detalle = models.CharField(max_length=45, db_column='detalle')

    class Meta:
        db_table = 'clase'
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'

    def __str__(self):
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre=self.nombre.lower()
        self.detalle=self.detalle.lower()
        super(Clase, self).save()

    def get_absolute_url():
        pass


class Asistencia(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.DO_NOTHING, db_column='clase_id')
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision_id')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante_credencial')
    fecha_hora = models.DateTimeField(db_column='fechahora')

    class Meta:
        unique_together = ['clase', 'estudiante', 'comision']
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return '{}-{}, {}'.format(self.clase.nombre.upper(), self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title())

    def save(self):
        super(Asistencia, self).save()

    def get_absolute_url():
        pass

class EvaluacionUnidad(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    unidad = models.ForeignKey(Unidad, on_delete=models.DO_NOTHING, db_column='unidad')
    aprobado = models.BooleanField(db_column='aprobado')

    class Meta:
        db_table = 'evaluacionunidad'
        verbose_name = 'Evaluacion de Unidad'
        verbose_name_plural = 'Evaluaciones de Unidades'

    def __str__(self):
        return '{}, {} - {}'.format(self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title(), self.unidad.nombre.upper())
    
    def save(self):
        super(EvaluacionUnidad, self).save()

    def get_absolute_url():
        pass


class Parcial(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    unidad = models.ForeignKey(Unidad, on_delete=models.DO_NOTHING, db_column='unidad')
    nota = models.IntegerField(db_column='nota')

    class Meta:
        db_table = 'parcial'
        verbose_name = 'Parcial'
        verbose_name_plural = 'Parciales'

    def __str__(self):
        return '{}, {} - {}'.format(self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title(), self.unidad.nombre.upper())

    def save(self):
        super(Parcial, self).save()

    def get_absolute_url():
        pass

class EvaluacionDiaria(models.Model):
    parcial = models.ForeignKey(Parcial, on_delete=models.DO_NOTHING, db_column='parcial')
    orden = models.IntegerField(db_column='orden')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    aprobado = models.BooleanField(db_column='aprobado')

    class Meta:
        db_table = 'evaluaciondiaria'
        verbose_name = 'Evaluacion Diaria'
        verbose_name_plural = 'Evaluaciones Diarias'

    def __str__(self):
        return '{}, {} ({})'.format(self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title(), self.parcial.unidad.nombre.upper())

    def save(self):
        super(EvaluacionDiaria, self).save()

    def get_absolute_url():
        pass
