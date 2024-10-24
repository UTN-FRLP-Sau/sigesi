from django.db import connection

df = open('/home/jronconi/escuelas_nuevas.sql', encoding='UTF-8')
lineas=df.readlines()

def run():
    cursor = connection.cursor()
    i=0
    j=len(lineas)
    for linea in lineas:
        try:
            cursor.execute(linea.lower())
        except Exception as error:
            i=i+1
            print(linea)
            print(error)
