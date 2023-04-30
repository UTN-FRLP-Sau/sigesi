from django.db import models

# Create your models here.

GESTION_ESCUELA_CHOICES = [("privada", "Privada"), ("publica", "Publica"),
                           ("mixta", "Mixta"),
                           ("social/cooperativa", "Social/Cooperativa")]

AMBITO_ESCUELA_CHOICES = [
    ("rural", "Rural"),
    ("urbano", "Urbano"),
]


class Pais(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_pais')
    id2l = models.CharField(max_length=2, db_column='id2L_Pais')
    id3l = models.CharField(max_length=3, db_column='id3L_Pais')
    nombre = models.CharField(max_length=50, db_column='nombre_pais')
    coord_1_cap = models.FloatField(db_column='coordenada1_pais')
    coord_2_cap = models.FloatField(db_column='coordenada2_pais')
    cod_telefonico = models.IntegerField(db_column='codTelefonico_pais')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'pais'

    def __str__(self):  #Python 3
        return '{}'.format(self.nombre)


class PartidoPBA(models.Model):
    id = models.CharField(max_length=5,
                          primary_key=True,
                          db_column='id_partido')
    nombre = models.CharField(max_length=50, db_column='nombre_partido')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        db_table = 'partidopba'

    def __str__(self):  #Python 3
        return '{}'.format(self.nombre)


class Provincia(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_provincia')
    nombre = models.CharField(max_length=50, db_column='nombre_provincia')
    pais = models.ForeignKey(Pais,
                             on_delete=models.DO_NOTHING,
                             db_column='pais_provincia')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        db_table = 'provincia'

    def __str__(self):  #Python 3
        return '{}'.format(self.nombre)


class Localidad(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_localidad')
    nombre = models.CharField(max_length=51, db_column='nombre_localidad')
    coord_1 = models.FloatField(db_column='coordenada1_localidad')
    coord_2 = models.FloatField(db_column='coordenada2_localidad')
    partido = models.ForeignKey(PartidoPBA,
                                on_delete=models.DO_NOTHING,
                                null=True,
                                blank=True,
                                db_column='PartidoPBA_localidad')
    provincia = models.ForeignKey(Provincia,
                                  on_delete=models.DO_NOTHING,
                                  db_column='provincia_localidad')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        db_table = 'localidad'

    def __str__(self):  #Python 3
        return '{}'.format(self.nombre)


class Escuela(models.Model):
    cue = models.CharField(max_length=12,
                           primary_key=True,
                           db_column='CUE_escuela')
    gestion = models.CharField(max_length=19,
                               choices=GESTION_ESCUELA_CHOICES,
                               db_column='gestion_escuela')
    ambito = models.CharField(max_length=7,
                              choices=AMBITO_ESCUELA_CHOICES,
                              db_column='ambito_escuela')
    tecnica = models.BooleanField(db_column='tecnica_escuela')
    nombre = models.CharField(max_length=150, db_column='nombre_escuela')
    domicilio = models.CharField(max_length=180, db_column='domicilio_escuela')
    coordenada_1 = models.FloatField(default=0,
                                     db_column='coordenada1_escuela')
    coordenada_2 = models.FloatField(default=0,
                                     db_column='coordenada2_escuela')
    localidad = models.ForeignKey(Localidad,
                                  on_delete=models.DO_NOTHING,
                                  db_column='localidad_escuela')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Escuela'
        verbose_name_plural = 'Escuelas'
        db_table = 'escuela'

    def __str__(self):  #Python 3
        return '{}-{}'.format(self.cue, self.nombre)


class Persona(models.Model):
    '''
    Faltan los campos:
    timeCreteStamp Podria ser una columna con fecha y otra con hora
    timeUpdateStamp Podria ser una columna con fecha y otra con hora
    '''
    id_persona = models.IntegerField(primary_key=True,
                                     auto_created=True,
                                     editable=False)
    apellido_1_persona = models.CharField(max_length=50)
    apellido_2_persona = models.CharField(max_length=50, null=True, blank=True)
    nombre_1_persona = models.CharField(max_length=50)
    nombre_2_persona = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento_persona = models.DateField()
    pais = models.ForeignKey(Pais,
                             on_delete=models.DO_NOTHING,
                             null=True,
                             blank=True)
    localidad = models.ForeignKey(Localidad,
                                  on_delete=models.DO_NOTHING,
                                  null=True,
                                  blank=True)
    cue = models.ForeignKey(Escuela,
                            on_delete=models.DO_NOTHING,
                            null=True,
                            blank=True)

    class Meta:
        ordering = ['apellido_1_persona']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'persona'

    def __str__(self):  #Python 3
        return '{} {}, {} {}'.format(self.apellido_1_persona,
                                     self.apellido_2_persona,
                                     self.nombre_1_persona,
                                     self.nombre_2_persona)


class TelefonoEscuela(models.Model):
    telefono = models.CharField(max_length=50, db_column='telefono_escuela')
    cue = models.ForeignKey(Escuela,
                            on_delete=models.DO_NOTHING,
                            db_column='id_escuela')

    class Meta:
        ordering = ['cue']
        verbose_name = 'Telefono de la Escuela'
        verbose_name_plural = 'Telefonos de las Escuelas'
        db_table = 'telefonoescuela'

    def __str__(self):  #Python 3
        return '{}-{}'.format(self.cue.cue, self.telefono)


class MailEscuela(models.Model):
    cue = models.ForeignKey(Escuela,
                            on_delete=models.DO_NOTHING,
                            db_column='id_escuela')
    mail = models.EmailField(max_length=254, db_column='mail_escuela')

    class Meta:
        ordering = ['cue']
        verbose_name = 'Correo Electronico de la Escuela'
        verbose_name_plural = 'Correos Electronicos de las Escuelas'
        db_table = 'mailescuela'

    def __str__(self):  #Python 3
        return '{}-{}'.format(self.cue.cue, self.mail)
