from django.db import models
import os
from uuid import uuid4

"""
Tabla imagenes, no entiendo xq todo es null, ni que es el tipo
CPA y CP4, cual tiene 4 digitos
"""


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
    # donde almacenar el archivo usando la fecha actual
    # año/mes/dia
    ruta = os.path.join('static/media/documentos', credencial)
    # Generamos el nombre del archivo con un idenfiticar
    # aleatorio y la extension del archivo original
    nombre_archivo = '{}.{}'.format(uuid4().hex,extension)
    # Retornamos la ruta completa
    return os.path.join(ruta, nombre_archivo)


class PartidoPBA(models.Model):
    id = models.CharField(max_length=5,
                          primary_key=True,
                          db_column='id')
    nombre = models.CharField(max_length=100, db_column='nombre')

    def save(self):
        self.nombre = self.nombre.lower()
        super(PartidoPBA, self).save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        db_table = 'partidopba'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())


class Pais(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=50, db_column='nombre')
    coord_x = models.FloatField(db_column='coordenadaX')
    coord_y = models.FloatField(db_column='coordenadaY')
    nacionalidad = models.CharField(max_length=100, db_column='nacionalidad')

    def save(self):
        self.nombre=self.nombre.lower()
        self.nacionalidad = self.nacionalidad.lower()
        super(Pais, self).save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'pais'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())


class Provincia(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=50, db_column='nombre')
    pais = models.ForeignKey(Pais,
                             on_delete=models.DO_NOTHING,
                             db_column='pais')

    def save(self):
        self.nombre=self.nombre.lower()
        super(Provincia, self).save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        db_table = 'provincia'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())


class Localidad(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    nombre = models.CharField(max_length=51, db_column='nombre')
    partido = models.ForeignKey(PartidoPBA,
                                on_delete=models.DO_NOTHING,
                                null=True,
                                blank=True,
                                db_column='Partido')
    provincia = models.ForeignKey(Provincia,
                                  on_delete=models.DO_NOTHING,
                                  db_column='provincia')

    def save(self):
        self.nombre=self.nombre.lower()
        super(Localidad,self).save()

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        db_table = 'localidad'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())


class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=50, db_column='tipo')

    def save(self):
        self.tipo = self.tipo.lower()
        super(TipoDocumento,self).save()

    class Meta:
        ordering=['tipo']
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        db_table = 'tipodocumento'

    def __str__(self):
        return '{}'.format(self.tipo.title())


class Persona(models.Model):
    apellidos = models.CharField(max_length=60, db_column='apellidos')
    nombres = models.CharField(max_length=60, db_column='nombres')
    fecha_nacimiento = models.DateField(db_column='nacimientofecha')
    pais_nacimiento = models.ForeignKey(Pais,
                                        on_delete=models.DO_NOTHING,
                                        related_name='nacimiento_pais',
                                        db_column='nacimientopais')
    nacionalidad = models.ForeignKey(Pais,
                                     on_delete=models.DO_NOTHING,
                                     related_name='pais_nacionalidad',
                                     db_column='nacionalidad')
    documento_tipo = models.ForeignKey(TipoDocumento,
                                       on_delete=models.DO_NOTHING,
                                       db_column='documentotipo')
    numero_documento = models.CharField(max_length=16, db_column='documentonumero')
    pais_documento = models.ForeignKey(Pais,
                                       on_delete=models.DO_NOTHING,
                                       related_name='documento_pais_emisor',
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
    correo = models.EmailField(max_length=254, db_column='email')

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

    class Meta:
        ordering = ['apellidos']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'persona'

    def __str__(self):  # Python 3
        return '{}, {}'.format(self.apellidos.upper(), self.nombres.title())

class Escuela(models.Model):
    cue = models.CharField(max_length=9,
                           primary_key=True,
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

    def save(self):
        self.gestion = self.gestion.lower()
        self.ambito = self.ambito.lower()
        self.nombre = self.nombre.lower()
        self.domicilio_calle = self.domicilio_calle.lower()
        self.domicilio_cpa = self.domicilio_cpa.lower()
        self.domicilio_cp4 = self.domicilio_cp4.lower()
        super(Escuela, self).save()


    class Meta:
        ordering = ['nombre']
        verbose_name = 'Escuela'
        verbose_name_plural = 'Escuelas'
        db_table = 'escuela'

    def __str__(self):  # Python 3
        return '{} ({})'.format(self.nombre.title(), self.cue)


class TelefonoEscuela(models.Model):
    telefono = models.CharField(max_length=50, db_column='telefono')
    escuela = models.ForeignKey(Escuela,
                            on_delete=models.DO_NOTHING,
                            db_column='escuela')

    def save(self):
        self.telefono = self.telefono.lower()
        super(TelefonoEscuela, self).save()

    class Meta:
        ordering = ['escuela']
        verbose_name = 'Telefono de la Escuela'
        verbose_name_plural = 'Telefonos de las Escuelas'
        db_table = 'telefonoEscuela'

    def __str__(self):  # Python 3
        return '{}-{}'.format(self.escuela.nombre, self.telefono)


class MailEscuela(models.Model):
    escuela = models.ForeignKey(Escuela,
                            max_length=9,
                            on_delete=models.DO_NOTHING,
                            db_column='escuela')
    mail = models.EmailField(max_length=254, db_column='mail')

    def save(self):
        self.mail=self.mail.lower()
        super(MailEscuela, self).save()

    class Meta:
        ordering = ['escuela']
        verbose_name = 'Correo Electronico de la Escuela'
        verbose_name_plural = 'Correos Electronicos de las Escuelas'
        db_table = 'mailescuela'

    def __str__(self):  # Python 3
        return '{}-{}'.format(self.escuela.nombre, self.mail)

class Genero(models.Model):
    nombre = models.CharField(db_column='nombre', max_length=45)

    def save(self):
        self.nombre = self.nombre.lower()
        super(Genero, self).save()

    class Meta:
        ordering=['nombre']
        db_table = 'genero'
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class Docente(models.Model):
    cbu = models.IntegerField(db_column='cbu')
    genero = models.ForeignKey(Genero, on_delete=models.DO_NOTHING, db_column='genero')
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        ordering=['persona']
        db_table = 'docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return '{}, {}'.format(self.persona.apellidos.upper(), self.persona.nombres.title())


class TituloSecundario(models.Model):
    titulo = models.CharField(max_length=45, db_column='titulo')
    tecnico = models.BooleanField(db_column='tecnico')

    def save(self):
        self.titulo = self.titulo.lower()
        super(TituloSecundario, self).save()

    class Meta:
        ordering=['titulo']
        db_table = 'tituloescuela'
        verbose_name = 'Titulo'
        verbose_name_plural = 'Titulos'

    def __str__(self):
        return '{}'.format(self.titulo.title())


class Estudiante(models.Model):
    credencial = models.IntegerField(primary_key=True, db_column='credencial')
    legajo = models.IntegerField(default=0, db_column='legajo')
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
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING, db_column='persona')

    def save(self):
        self.nombre_autopercibido = self.nombre_autopercibido.lower()
        self.titulo_secundario = self.titulo_secundario.lower()
        self.emergencia_contacto = self.emergencia_contacto.lower()
        super(Estudiante, self).save()

    class Meta:
        ordering=['credencial']
        db_table = 'estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantess'

    def __str__(self):
        return '{}, {}'.format(self.persona.apellidos.upper(), self.persona.nombres.title())


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


class Aula(models.Model):
    nombre = models.CharField(db_column='denominacion', max_length=20)
    capacidad = models.IntegerField(db_column='capacidad')
    aire = models.BooleanField(db_column='aire')
    proyector = models.BooleanField(db_column='proyector')
    accesibilidad = models.BooleanField(db_column='accesibiliad')

    def save(self):
        self.nombre = self.nombre.lower()
        super(Aula, self).save()

    class Meta:
        ordering=['nombre']
        db_table = 'aula'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class ModalidadCursado(models.Model):
    nombre = models.CharField(max_length=15, db_column='nombre')
    descripcion = models.CharField(max_length=150, db_column='descripcion')

    def save(self):
        self.nombre = self.nombre.lower()
        self.descripcion = self.descripcion.lower()

    class Meta:
        db_table = 'modalidadcursada'
        verbose_name = 'Modalidad'
        verbose_name_plural = 'Modalidades'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class Comision(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING, db_column='aula')
    nombre = models.CharField(max_length=4, db_column='nombre')
    modalidad = models.ForeignKey(ModalidadCursado, on_delete=models.DO_NOTHING, db_column='modalidadcursada')
    ingreso_anio = models.IntegerField(db_column='ingresoanio')
    estudiante = models.ManyToManyField(Estudiante)

    def save(self):
        self.nombre = self.nombre.lower()
        super(Comision, self).save()

    class Meta:
        ordering = ['ingreso_anio','nombre']
        db_table = 'comision'
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'

    def __str__(self):
        return '{}-{}'.format(self.nombre.upper(), self.ingreso_anio)

'''
class Matricula(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante', primary_key=True)
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision', primary_key=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'comision'],
                name='unique_combination_estudiante_comision'
                )]
        db_table = 'matricula'
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'

    def __str__(self):
        return '{}, {} ({})'.format(self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title(), self.comision.nombre.upper())
'''

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


class Unidad(models.Model):
    nombre = models.CharField(max_length=45, db_column='nombre')
    detalle = models.CharField(max_length=100, db_column='detalle')

    def save(self):
        self.nombre=self.nombre.lower()
        self.detalle=self.detalle.lower()
        super(Unidad, self).save()

    class Meta:
        db_table = 'unidad'
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class Clase(models.Model):
    nombre = models.CharField(max_length=45, db_column='nombre')
    detalle = models.CharField(max_length=45, db_column='detalle')

    def save(self):
        self.nombre=self.nombre.lower()
        self.detalle=self.detalle.lower()
        super(Clase, self).save()

    class Meta:
        db_table = 'clase'
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class Asistencia(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.DO_NOTHING, db_column='clase_id')
    comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='comision_id')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante_credencial')
    fecha_hora = models.DateTimeField(db_column='fechahora')

    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return '{}-{}, {}'.format(self.clase.nombre.upper(), self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title())


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


class EvaluacionDiaria(models.Model):
    parcial = models.ForeignKey(Parcial, on_delete=models.DO_NOTHING, db_column='parcial')
    orden = models.IntegerField(db_column='orden')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    aprobado = models.BooleanField(db_column='aprobado')

    class Meta:
        db_table = 'evaluacionesdiarias'
        verbose_name = 'Evaluacion Diaria'
        verbose_name_plural = 'Evaluaciones Diarias'

    def __str__(self):
        return '{}, {} ({})'.format(self.estudiante.persona.apellidos.upper(), self.estudiante.persona.nombres.title(), self.parcial.unidad.nombre.upper())
