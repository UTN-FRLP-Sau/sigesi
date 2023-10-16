from django.db import connection

df = open('C:/Users/jorge/OneDrive/Escritorio/Github/sigesi/src/scripts/CargarEscuelas2.sql', encoding='UTF-8')
lineas=df.readlines()

def run():
    cursor = connection.cursor()
    for linea in lineas:
        try:
            cursor.execute(linea)
        except:
            print(linea)
