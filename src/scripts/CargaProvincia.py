from apps.inscripcion.models import Provincia
from apps.inscripcion.models import Pais

Values_provincias = ((2, 'Ciudad de Buenos Aires', 9),
                     (6, 'Buenos Aires', 9),
                     (10, 'Catamarca', 9),
                     (14, 'Córdoba', 9),
                     (18, 'Corrientes', 9),
                     (22, 'Chaco', 9),
                     (26, 'Chubut', 9),
                     (30, 'Entre Ríos', 9),
                     (34, 'Formosa', 9),
                     (38, 'Jujuy', 9),
                     (42, 'La Pampa', 9),
                     (46, 'La Rioja', 9),
                     (50, 'Mendoza', 9),
                     (54, 'Misiones', 9),
                     (58, 'Neuquén', 9),
                     (62, 'Río Negro', 9),
                     (66, 'Salta', 9),
                     (70, 'San Juan', 9),
                     (74, 'San Luis', 9),
                     (78, 'Santa Cruz', 9),
                     (82, 'Santa Fe', 9),
                     (86, 'Santiago del Estero', 9),
                     (90, 'Tucumán', 9),
                     (94, 'Tierra del Fuego', 9)
                     )


def run():
    Provincia.objects.all().delete()

    for x in Values_provincias:
        pais = Provincia(
            id = x[0],
            nombre = x[1],
            pais = Pais.objects.get(id=x[2])
            )

        pais.save()
