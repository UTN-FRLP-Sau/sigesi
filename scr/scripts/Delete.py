from apps.core.models import Pais, PartidoPBA, Provincia, Localidad, Escuela, MailEscuela, TelefonoEscuela


def run():
    TelefonoEscuela.objects.all().delete()
    MailEscuela.objects.all().delete()
    Escuela.objects.all().delete()
    Localidad.objects.all().delete()
    Provincia.objects.all().delete()
    PartidoPBA.objects.all().delete()
    Pais.objects.all().delete()
