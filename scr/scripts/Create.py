from .CargaPais import run as Pais
from .CargaPartido import run as Partido
from .CargaProvincia import run as Provincia
from .CargaEscuela import run as Escuela
from .CargaTelefono import run as Telefono
from .CargaMail import run as Mail
from .CargaLocalidad import run as Localidad
from .Delete import run as Delete


def run():
    Delete()
    Pais()
    Partido()
    Provincia()
    Localidad()
    Escuela()
    Mail()
    Telefono()
