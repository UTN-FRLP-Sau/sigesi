from apps.core.models import Provincia

Values_provincias = ((2, 'Ciudad de Buenos Aires',
                      32), (6, 'Buenos Aires', 32), (10, 'Catamarca', 32),
                     (14, 'Córdoba', 32), (18, 'Corrientes', 32),
                     (22, 'Chaco', 32), (26, 'Chubut', 32),
                     (30, 'Entre Ríos', 32), (34, 'Formosa', 32),
                     (38, 'Jujuy', 32), (42, 'La Pampa', 32), (46, 'La Rioja',
                                                               32),
                     (50, 'Mendoza', 32), (54, 'Misiones',
                                           32), (58, 'Neuquén',
                                                 32), (62, 'Río Negro', 32),
                     (66, 'Salta', 32), (70, 'San Juan',
                                         32), (74, 'San Luis',
                                               32), (78, 'Santa Cruz',
                                                     32), (82, 'Santa Fe', 32),
                     (86, 'Santiago del Estero',
                      32), (90, 'Tucumán', 32), (94, 'Tierra del Fuego', 32))


def run():
    Provincia.objects.all().delete()

    for x in Values_provincias:
        pais = Provincia(x[0], x[1], x[2])

        pais.save()
