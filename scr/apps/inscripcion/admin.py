from django.contrib import admin

# Register your models here.
from apps.inscripcion.models import (Pais, PartidoPBA, Provincia, Localidad, Escuela,
                                     Persona, TelefonoEscuela, MailEscuela)

'''
class PaisAdmin(admin.ModelAdmin):
    list_display = []


class PartidoPBAAdmin(admin.ModelAdmin):
    pass


class ProvinciaAdmin(admin.ModelAdmin):
    pass


class LocalidadAdmin(admin.ModelAdmin):
    pass


class EscuelaAdmin(admin.ModelAdmin):
    pass


class PersonaAdmin(admin.ModelAdmin):
    pass


class TelefonoEscuelaAdmin(admin.ModelAdmin):
    pass


class MailEscuelaAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


# Register your models here.

admin.site.register(Pais, PaisAdmin)
admin.site.register(PartidoPBA, PartidoPBAAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(TelefonoEscuela, TelefonoEscuelaAdmin)
admin.site.register(MailEscuela, MailEscuelaAdmin)
'''
