from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from apps.inscripcion.models import (
                                    PartidoPBA,
                                    Pais,
                                    Provincia,
                                    Localidad,
                                    TipoDocumento,
                                    Persona,
                                    Escuela,
                                    TelefonoEscuela,
                                    MailEscuela,
                                    Genero,
                                    Docente,
                                    TituloSecundario,
                                    Estudiante,
                                    Archivos,
                                    Aula,
                                    ModalidadCursado,
                                    Comision,
                                    EquipoDocente,
                                    Unidad,
                                    Clase,
                                    Asistencia,
                                    EvaluacionUnidad,
                                    Parcial,
                                    EvaluacionDiaria,
                                    Documentacion,
                                    Inscripcion,
                                    Curso
)

# Register your models here.


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombres', 'numero_documento', 'correo', 'especialidad',
                    'modalidad', 'turno', 'inscripcion_curso', 'cambiar_curso')
    search_fields = ('persona__nombres', 'persona__apellidos', 'persona__numero_documento')
    list_filter=('especialidad',)

    # Define los métodos personalizados para las columnas renombradas
    def apellidos(self, obj):
        return obj.persona.apellidos.upper()
    apellidos.admin_order_field = 'persona__apellidos'
    apellidos.short_description = 'Apellidos'

    def nombres(self, obj):
        return obj.persona.nombres.title()
    nombres.admin_order_field = 'persona__nombres'
    nombres.short_description = 'Nombres'

    def numero_documento(self, obj):
        return obj.persona.numero_documento
    numero_documento.admin_order_field = 'persona__numero_documento'
    numero_documento.short_description = 'Número de Documento'

    def correo(self, obj):
        return obj.persona.correo
    correo.admin_order_field = 'persona__correo'
    correo.short_description = 'Correo'

    def especialidad(self, obj):
        return obj.get_especialidad_display()
    especialidad.admin_order_field = 'especialidad'
    especialidad.short_description = 'Especialidad'

    def modalidad(self, obj):
        return obj.get_modalidad_display()
    modalidad.admin_order_field = 'modalidad'
    modalidad.short_description = 'Modalidad'

    def turno(self, obj):
        return obj.get_turno_display()
    turno.admin_order_field = 'turno'
    turno.short_description = 'Turno'
    
    # Columna para mostrar si está inscrito
    def inscripcion_curso(self, obj):
        inscripcion = Inscripcion.objects.filter(
            estudiante=obj).first()
        return inscripcion.estado if inscripcion else "No inscrito"
    inscripcion_curso.short_description = 'Curso Actual'
    inscripcion_curso.admin_order_field = 'inscripcion_curso'
    
    # Campo con menú desplegable para cambiar curso
    def cambiar_curso(self, obj):
        inscripcion = Inscripcion.objects.all()
        cursos = Curso.objects.all()

        if inscripcion:
            options = ''.join(
                f'<option value="{curso.id}" {
                    "selected" if curso == inscripcion.curso else ""}>{curso.nombre}</option>'
                for curso in cursos
            )
            # Genera un menú desplegable y un botón para enviar el cambio
            html = f'''
            <select onchange="cambiarCurso(this, {obj.pk})">
                {options}
            </select>
            '''
            return mark_safe(html)
        return "No inscrito"
    cambiar_curso.admin_order_field = 'cambiar_curso'
    cambiar_curso.short_description = 'Cambiar Curso'
    
    class Media:
        js = ('admin/js/cambiar_curso.js',)
    



admin.site.register(PartidoPBA)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(TipoDocumento)
admin.site.register(Persona)
admin.site.register(Escuela)
admin.site.register(TelefonoEscuela)
admin.site.register(MailEscuela)
admin.site.register(Genero)
#admin.site.register(Docente)
#admin.site.register(TituloSecundario)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Archivos)
#admin.site.register(Aula)
admin.site.register(ModalidadCursado)
#admin.site.register(Comision)
#admin.site.register(EquipoDocente)
#admin.site.register(Unidad)
#admin.site.register(Clase)
#admin.site.register(Asistencia)
#admin.site.register(EvaluacionUnidad)
#admin.site.register(Parcial)
admin.site.register(Curso)
admin.site.register(Inscripcion)
#admin.site.register(EvaluacionDiaria)
#admin.site.register(Documentacion)
