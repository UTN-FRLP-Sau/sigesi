import pandas as pd
from django.db import connection

df = open('C:/Users/CIVIL/Desktop/SUI/inscripcion/src/scripts/CargarEscuelas2.csv', encoding='UTF-8')
lineas=df.readlines()

def run():
    cursor = connection.cursor()
    for linea in lineas:
        try:
            cursor.execute(linea)
        except:
            print(linea)
