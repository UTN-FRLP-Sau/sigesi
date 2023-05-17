import environ
# from django.urls import reverse_lazy
import os

# Inicializamos la variable de entorno
env = environ.Env()
environ.Env.read_env()


def run():
    print(str(env('ALLOWED_HOSTS')).split(','))
    print([str(env('ALLOWED_HOSTS')).split(',')])


