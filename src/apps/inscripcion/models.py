# future

# Librerias Standars
import os
from uuid import uuid4
from datetime import date
import re

# Librerias de Terceros

# Django
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

# Django Locales
from .validators import validate_file_extension

# Create your models here.

GESTION_ESCUELA_CHOICES = [("privado", "Privado"),
                           ("estatal", "Estatal"),
                           ("social/cooperativa", "Social/Cooperativa")]

AMBITO_ESCUELA_CHOICES = [
    ("rural", "Rural"),
    ("urbano", "Urbano"),
    ("rural agrupado", "Rural Agrupado"),
    ("Rural disperso", "Rural Disperso")
]

SEXO_ESTUDIANTE_CHOICES = [
    ("m", "Masculino"),
    ("f", "Femenino"),
    ("n", "No Binario")
]

ESPECIALIDAD_ESTUDIANTE_CHOICES = [
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

TURNO_INGRESO_CHOICES = [
    ("m", "Turno Mañana"),
    ("t", "Turno Tarde"),
    ("n", "Turno Noche"),
]

MODALIDAD_CHOICES = [
    ('p', "Presencial"),
    ('s', "Semi-Presencial"),
    ('l', "Libre"),
]

PERIODO_CHOICES = [
    ('e', "Extensivo - Agosto-Diciembre"),
    ('i', "Intensivo - Febrero-Marzo"),
]


def _generar_ruta_documento(instance, filename, path):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Generamos la ruta relativa a media_root en funcion del a
    ruta_relativa = date.today().strftime('%y/%m/%d')
    # Obtenemos una instancia de Storage
    storage = default_storage
    # Validacion y normalizacion de la ruta
    ruta_validada = 'documentos'
    # Verificamos que la ruta sea segura y este dentro del directorio permitido MEDIA_ROOT
    if not storage.exists(ruta_validada):
        # La ruta esta fuera del directorio permitido
        raise ValueError("Ruta invalida")
    # Generamos el nombre del archivo con un idenfiticar aleatorio y la extension del archivo original
    nombre_archivo = '{}.{}'.format(uuid4().hex, extension)
    # Retornamos la ruta completa
    return os.path.join(ruta_validada, ruta_relativa, nombre_archivo)


class Pais(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', unique=True)
    nombre = models.CharField(max_length=50, db_column='nombre', unique=True)
    coord_x = models.FloatField(db_column='coordenadaX')
    coord_y = models.FloatField(db_column='coordenadaY')
    nacionalidad = models.CharField(max_length=100, db_column='nacionalidad')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'pais'

    def __str__(self):  # Python 3
        return '{}'.format(self.nombre.title())

    def save(self):
        self.nombre = self.nombre.lower()
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
        self.nombre = self.nombre.lower()
        super(Provincia, self).save()

    def get_absolute_url():
        pass


class PartidoPBA(models.Model):
    id = models.CharField(max_length=5,
                          primary_key=True,
                          unique=True,
                          db_column='id')
    nombre = models.CharField(max_length=100, db_column='nombre', unique=True)
    provincia = models.ForeignKey(Provincia,
                                  on_delete=models.DO_NOTHING,
                                  db_column='provincia')

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
        self.nombre = self.nombre.lower()
        super(Localidad, self).save()

    def get_absolute_url():
        pass


class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=50, db_column='tipo', unique=True)

    class Meta:
        ordering = ['tipo']
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        db_table = 'tipodocumento'

    def __str__(self):
        return '{}'.format(self.tipo.title())

    def save(self):
        self.tipo = self.tipo.lower()
        super(TipoDocumento, self).save()

    def get_absolute_url():
        pass


class Genero(models.Model):
    nombre = models.CharField(db_column='nombre', max_length=45, unique=True)

    class Meta:
        ordering = ['nombre']
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


class Persona(models.Model):
    apellidos = models.CharField(max_length=60, db_column='apellidos')
    nombres = models.CharField(max_length=60, db_column='nombres')
    nombre_autopercibido = models.CharField(
        max_length=60, db_column='nombreautopercibido', null=True, blank=True)
    fecha_nacimiento = models.DateField(db_column='nacimientofecha')
    sexo = models.CharField(max_length=1,
                            db_column='sexo',
                            choices=SEXO_ESTUDIANTE_CHOICES)
    genero = models.ForeignKey(Genero,
                               on_delete=models.DO_NOTHING,
                               db_column='genero')
    genero_otro = models.CharField(
        max_length=100, db_column='genero_otro', null=True, blank=True)
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
    numero_documento = models.CharField(
        max_length=16, db_column='documentonumero', unique=True)
    cuil = models.CharField(max_length=13, null=True,
                            blank=True, db_column='cuil')
    pais_documento = models.ForeignKey(Pais,
                                       on_delete=models.DO_NOTHING,
                                       related_name='pais_documento_emisor',
                                       db_column='documentopaisemisor')
    domicilio_pais = models.ForeignKey(Pais,
                                       on_delete=models.DO_NOTHING,
                                       related_name='pais_domicilio',
                                       db_column='domiciliopais')
    domicilio_calle = models.CharField(max_length=100,
                                       default=None,
                                       null=True,
                                       blank=True,
                                       db_column='domiciliocalle')
    domicilio_altura = models.CharField(max_length=10,
                                        default=None,
                                        null=True,
                                        blank=True,
                                        db_column='domicilioaltura')
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
                                            null=True,
                                            blank=True,
                                            on_delete=models.DO_NOTHING,
                                            db_column='domiciliolocalidad')
    domicilio_cpa = models.CharField(max_length=8,
                                     db_column='domicilioCPA',
                                     null=True,
                                     blank=True)
    domicilio_cp4 = models.CharField(max_length=4,
                                     db_column='domicilioCP4',
                                     null=True,
                                     blank=True)
    domicilio_coordenada_x = models.FloatField(db_column='domiciliocoordenadaX',
                                               null=True,
                                               blank=True)
    domicilio_coordenada_y = models.FloatField(db_column='domiciliocoordenadaY',
                                               null=True,
                                               blank=True)
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
        self.apellidos = self.apellidos.lower()
        self.nombres = self.nombres.lower()
        self.nombre_autopercibido = self.nombre_autopercibido.lower(
        ) if self.nombre_autopercibido is not None else None
        self.genero_otro = self.genero_otro.lower(
        ) if self.genero_otro is not None else None
        self.numero_documento = self.numero_documento.lower()
        self.domicilio_altura = self.domicilio_altura.lower(
        ) if self.domicilio_altura is not None else None
        self.domicilio_piso = self.domicilio_piso.lower(
        ) if self.domicilio_piso is not None else None
        self.domicilio_departamento = self.domicilio_departamento.lower(
        ) if self.domicilio_departamento is not None else None
        self.domicilio_barrio = self.domicilio_barrio.lower(
        ) if self.domicilio_barrio is not None else None
        self.domicilio_cpa = self.domicilio_cpa.lower(
        ) if self.domicilio_cpa is not None else None
        self.domicilio_cp4 = self.domicilio_cp4.lower(
        ) if self.domicilio_cp4 is not None else None
        self.telefono = str(self.telefono).lower(
        ) if self.telefono is not None else None
        self.correo = self.correo.lower() if self.correo is not None else None
        # Damos el formato de cuil de la forma XX-XXXXXXXX-X
        if self.cuil is not None:
            patron = r'^\d{2}-\d{8}-\d$'
            cuil = self.cuil
            cuil = cuil.replace("-", "")
            if re.match(patron, cuil):
                self.cuil = cuil[:2]+'-'+cuil[2:11]+'-'+cuil[11:]
        else:
            self.cuil = None
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
    nombre = models.CharField(max_length=200,
                              db_column='nombre')
    domicilio_calle = models.CharField(max_length=200,
                                       db_column='domiciliocalle')
    domicilio_altura = models.IntegerField(db_column='domicilioaltura')
    domicilio_localidad = models.ForeignKey(Localidad,
                                            on_delete=models.DO_NOTHING,
                                            db_column='domiciliolocalidad')
    domicilio_cpa = models.CharField(max_length=8, db_column='domicilioCPA')
    domicilio_cp4 = models.CharField(max_length=4, db_column='domicilioCP4')
    domicilio_coordenada_x = models.FloatField(
        default=0, db_column='domiciliocoordenadaX')
    domicilio_coordenada_y = models.FloatField(
        default=0, db_column='domiciliocoordenadaY')

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
        self.mail = self.mail.lower()
        super(MailEscuela, self).save()

    def get_absolute_url():
        pass


class Docente(models.Model):
    cbu = models.IntegerField(db_column='cbu', unique=True)
#    comprobante = models.FileField(db_column='comprobante', upload_to=_generar_ruta_documento)
    persona = models.ForeignKey(
        Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        ordering = ['persona']
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
        ordering = ['titulo']
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
    credencial = models.AutoField(primary_key=True, db_column='credencial')
    legajo = models.IntegerField(default=0, db_column='legajo')
    escuela = models.ForeignKey(
        Escuela, on_delete=models.DO_NOTHING, db_column='escuela', blank=True, null=True)
    anio_egreso = models.IntegerField(db_column='escuelaanioegreso')
    titulo_secundario = models.CharField(
        max_length=150, db_column='tituloescuela')
    # titulo_secundario = models.ForeignKey(TituloSecundario, db_column='tituloescuela', on_delete=models.DO_NOTHING)
    emergencia_telefono = models.CharField(
        max_length=20, db_column='emergenciatelefono')
    emergencia_contacto = models.CharField(
        max_length=60, db_column='emergenciacontacto')
    especialidad = models.IntegerField(
        choices=ESPECIALIDAD_ESTUDIANTE_CHOICES, db_column='especialidad')
    turno = models.CharField(
        max_length=1, db_column='turno', choices=TURNO_ESTUDIANTE_CHOICES)
    modalidad = models.CharField(
        max_length=1, choices=MODALIDAD_CHOICES, db_column='modalidad')
    persona = models.OneToOneField(
        Persona, on_delete=models.DO_NOTHING, db_column='persona')

    class Meta:
        ordering = ['credencial']
        db_table = 'estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return '{}, {}'.format(self.persona.apellidos.upper(), self.persona.nombres.title())

    def save(self):
        # Guardamos todo en minusculas
        self.titulo_secundario = self.titulo_secundario.lower(
        ) if self.titulo_secundario is not None else None
        self.emergencia_contacto = self.emergencia_contacto.lower(
        ) if self.emergencia_contacto is not None else None

        super(Estudiante, self).save()
        
    def get_turno_display(self):
        return dict(TURNO_INGRESO_CHOICES).get(self.turno, "")
    
    def get_especialidad_display(self):
        return dict(ESPECIALIDAD_ESTUDIANTE_CHOICES).get(self.especialidad, "")
    
    def get_modalidad_display(self):
        return dict(MODALIDAD_CHOICES).get(self.modalidad, "")

    def get_absolute_url(self):
        pass


def _generar_ruta_documento(instance, filename):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Obtener el ultimo ID del modelo Archivos
    last_id = Archivos.objects.last().pk if Archivos.objects.exists() else 0
    # Generamos la ruta relativa a media_root en funcion del numero_documento
    ruta_relativa = str(instance.persona.numero_documento).lower()
    # Obtenemos una instancia de Storage
    # storage = default_storage
    # Validacion y normalizacion de la ruta
    ruta_validada = 'documentos'
    # Generamos el nombre del archivo con un idenfiticar aleatorio y la extension del archivo original
    nombre_archivo = '{}_{}.{}'.format(last_id, instance.tipo, extension)
    # Retornamos la ruta completa
    return os.path.join(ruta_validada, ruta_relativa, nombre_archivo)


class Archivos(models.Model):
    '''
    estado: 0- En revision
            1- Aprobado
            2- Rechazado
    '''
    tipo = models.CharField(max_length=20, db_column='tipo')
    path = models.FileField(db_column='ubicacion', upload_to=_generar_ruta_documento, validators=[
                            validate_file_extension])
    persona = models.ForeignKey(
        Persona, on_delete=models.DO_NOTHING, db_column='persona')
    estado = models.IntegerField(default=0, db_column='estado')

    class Meta:
        db_table = 'imagenes'
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return '({}) - {}, {}'.format(self.id, self.persona.apellidos.upper(), self.persona.nombres.title())

    def save(self):
        super(Archivos, self).save()

    def get_absolute_url():
        pass

    def clean(self):
        # Realizar la validación del tipo de archivo solo si hay un archivo adjunto
        if self.path:
            try:
                validate_file_extension(self.path)
            except ValidationError as e:
                raise ValidationError(
                    {'path': 'El archivo debe ser PDF, no se acepta otra extension'})


class Aula(models.Model):
    nombre = models.CharField(db_column='denominacion',
                              max_length=20, unique=True)
    capacidad = models.IntegerField(db_column='capacidad')
    aire = models.BooleanField(db_column='aire')
    proyector = models.BooleanField(db_column='proyector')
    accesibilidad = models.BooleanField(db_column='accesibiliad')

    class Meta:
        ordering = ['nombre']
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

    #def save(self):
    #    self.nombre = self.nombre.lower()
    #    self.descripcion = self.descripcion.lower()
    #    super(ModalidadCursado, self).save()

    def get_absolute_url():
        pass
    

class Comision(models.Model):
    aula = models.ForeignKey(
        Aula, on_delete=models.DO_NOTHING, db_column='aula')
    nombre = models.CharField(max_length=4, db_column='nombre')
    modalidad = models.ForeignKey(
        ModalidadCursado, on_delete=models.DO_NOTHING, db_column='modalidadcursada')
    ingreso_anio = models.IntegerField(db_column='ingresoanio')
    estudiante = models.ManyToManyField(Estudiante, db_table='matricula')

    class Meta:
        unique_together = ['nombre', 'ingreso_anio']
        ordering = ['ingreso_anio', 'nombre']
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
    comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='comision')
    docente = models.ForeignKey(
        Docente, on_delete=models.DO_NOTHING, db_column='docente')
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
        self.nombre = self.nombre.lower()
        self.detalle = self.detalle.lower()
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
        self.nombre = self.nombre.lower()
        self.detalle = self.detalle.lower()
        super(Clase, self).save()

    def get_absolute_url():
        pass


class Asistencia(models.Model):
    clase = models.ForeignKey(
        Clase, on_delete=models.DO_NOTHING, db_column='clase_id')
    comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='comision_id')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante_credencial')
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
    comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='comision')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    unidad = models.ForeignKey(
        Unidad, on_delete=models.DO_NOTHING, db_column='unidad')
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
    comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='comision')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
    unidad = models.ForeignKey(
        Unidad, on_delete=models.DO_NOTHING, db_column='unidad')
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
    parcial = models.ForeignKey(
        Parcial, on_delete=models.DO_NOTHING, db_column='parcial')
    orden = models.IntegerField(db_column='orden')
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.DO_NOTHING, db_column='estudiante')
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


def _generar_ruta_file_documento(instance, filename):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Obtener el ultimo ID del modelo Documentacion
    last_id = Documentacion.objects.last().pk if Documentacion.objects.exists() else 0
    # Generamos la ruta relativa a media_root en funcion del num_documento
    ruta_relativa = str(instance.num_documento).lower()
    # Obtenemos una instancia de Storage
    storage = default_storage
    # Validacion y normalizacion de la ruta
    ruta_validada = 'documentos'
    # Generamos el nombre del archivo con un idenfiticar aleatorio y la extension del archivo original
    nombre_archivo = '{}_{}.{}'.format(last_id, 'identificacion', extension)
    # Retornamos la ruta completa
    return os.path.join(ruta_validada, ruta_relativa, nombre_archivo)


def _generar_ruta_file_certificado(instance, filename):
    # Extraer extension del fichero
    extension = os.path.splitext(filename)[1][1:]
    # Obtener el ultimo ID del modelo Documentacion
    last_id = Documentacion.objects.last().pk if Documentacion.objects.exists() else 0
    # Generamos la ruta relativa a media_root en funcion del num_documento
    ruta_relativa = str(instance.num_documento).lower()
    # Obtenemos una instancia de Storage
    storage = default_storage
    # Validacion y normalizacion de la ruta
    ruta_validada = 'documentos'
    # Generamos el nombre del archivo con un idenfiticar aleatorio y la extension del archivo original
    nombre_archivo = '{}_{}.{}'.format(last_id, 'certificado', extension)
    # Retornamos la ruta completa
    return os.path.join(ruta_validada, ruta_relativa, nombre_archivo)


class Documentacion(models.Model):
    num_documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(max_length=254, unique=True)
    file_documento = models.FileField(
        upload_to=_generar_ruta_file_documento, validators=[validate_file_extension])
    file_certificado = models.FileField(
        upload_to=_generar_ruta_file_certificado, validators=[validate_file_extension])
    modalidad = models.CharField(
        choices=[choices for choices in MODALIDAD_CHOICES if choices[0] != ''], max_length=1)
    periodo = models.CharField(
        choices=[choices for choices in PERIODO_CHOICES if choices[0] != 'e'], max_length=1)
    turno = models.CharField(choices=[
                             choices for choices in TURNO_INGRESO_CHOICES if choices[0] != 'n'], max_length=1, default="m")
    aprobada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Documentacion'
        verbose_name_plural = 'Documentaciones'

    def __str__(self):
        return '{}'.format(self.num_documento)

    def save(self):
        # Borramos los puntos y espacios de los numeros de documentos
        num_documento = self.num_documento
        # Borramos los espacios finales e iniciales
        num_documento = num_documento.strip(" ")
        num_documento = num_documento.replace(".", "")  # Borramos los puntos
        self.num_documento = num_documento.replace(
            " ", "")  # Borramos los espacios finales
        super(Documentacion, self).save()

    def get_absolute_url(self):
        return reverse("documentacion_mostrar", kwargs={"pk": self.pk})


def generar_choices():
    from datetime import datetime
    meses_esp = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    choices = []
    anio_actual = datetime.now().year
    for anio in range(anio_actual, anio_actual + 2):
        for mes in range(1, 13):
            mes_nombre = meses_esp[datetime(
                1900, mes, 1).strftime('%B')].capitalize()
            choices.append((f"{mes_nombre}-{anio}", f"{mes_nombre}-{anio}"))
    return choices


class Turno(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return '{}'.format(self.nombre.title())
    

class Especialidad(models.Model):
    id = models.IntegerField(primary_key=True, editable=True)
    nombre = models.CharField(max_length=50)
    turno = models.ManyToManyField(Turno)

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return '{}'.format(self.nombre.title())



class Curso(models.Model):
    # Define los choices generados dinámicamente
    MESES_ANIOS_CHOICES = generar_choices()

    nombre = models.CharField(max_length=50)
    año = models.IntegerField()
    inscripcion_inicio = models.DateField(auto_now=False, auto_now_add=False)
    inscripcion_cierre = models.DateField(auto_now=False, auto_now_add=False)
    fecha_finalizacion = models.DateField(auto_now=False, auto_now_add=False)
    periodo_inicio = models.CharField(max_length=15, choices=MESES_ANIOS_CHOICES)
    periodo_cierre = models.CharField(max_length=15, choices=MESES_ANIOS_CHOICES)
    modalidad = models.ManyToManyField(ModalidadCursado)
    turno = models.ManyToManyField(Turno)
    

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return '{}'.format(self.nombre.title())


class Inscripcion(models.Model):
    ESTADOS_CHOICES = [
        ("inscripto", "Inscripto"),
        ("libre", "Libre"),
        ("aprobado", "Aprobado"),
        ("desaprobado", "Desaprobado"),
    ]
    estudiante = models.ForeignKey(
        'Estudiante', related_name='estudiante', on_delete=models.CASCADE)
    curso = models.ForeignKey(
        'Curso', related_name='curso', on_delete=models.CASCADE)
    especialidad = models.ForeignKey(
        'Especialidad', related_name='especialidad', on_delete=models.CASCADE)
    modalidad = models.ForeignKey(
        'ModalidadCursado', related_name='modalidad', on_delete=models.CASCADE)
    turno = models.ForeignKey('Turno', related_name='turno', on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, choices=ESTADOS_CHOICES)
    
    def especialidad_display(self):
        return dict(ESPECIALIDAD_ESTUDIANTE_CHOICES).get(self.especialidad, "")
    
    def estado_display(self):
        return dict(self.ESTADOS_CHOICES).get(self.estado, "")
    
    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return '{}({})({})'.format(self.estudiante.persona.apellidos.upper(), self.curso.nombre.title(), self.modalidad.nombre.title())
