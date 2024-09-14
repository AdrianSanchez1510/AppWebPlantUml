#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import models
import requests
from django.shortcuts import render

class ConexionBD(models.Model):
    tipo_base_datos = models.CharField(max_length=50)
    host = models.CharField(max_length=100)
    puerto = models.CharField(max_length=10)
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    nombre_base_datos = models.CharField(max_length=100)

def obtener_tablas(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'nombre_esquema'")
    return cursor.fetchall()


def generar_codigo_plantuml(tablas, columnas):
    codigo = "@startuml\n"
    for tabla in tablas:
        codigo += f"class {tabla['nombre']} {{\n"
        for columna in columnas[tabla['nombre']]:
            codigo += f"  {columna['nombre']} : {columna['tipo']}\n"
        codigo += "}\n"
    codigo += "@enduml"
    return codigo



def obtener_imagen_plantuml(codigo_plantuml):
    url_plantuml = "http://www.plantuml.com/plantuml/png/"
    response = requests.post(url_plantuml, data=codigo_plantuml)
    if response.status_code == 200:
        return response.url
    else:
        return None
    
def mostrar_diagrama(request):
    imagen_url = obtener_imagen_plantuml(codigo_plantuml)
    return render(request, 'mostrar_diagrama.html', {'imagen_url':imagen_url})


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagrama_uml.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
