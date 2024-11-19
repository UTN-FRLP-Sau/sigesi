# templatetags/fecha_filters.py
from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='formatear_fecha')
def formatear_fecha(value):
    try:
        fecha_obj = datetime.strptime(value, "%m_%Y")
        return fecha_obj.strftime("%B-%Y")  # %B da el nombre completo del mes
    except ValueError:
        return value  # Si la fecha no tiene el formato esperado, devolvemos el valor original
