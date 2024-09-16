from django.shortcuts import render
from .services import generar_codigo_plantuml, obtener_imagen_plantuml

def mostrar_diagrama(request):
    # Aquí debes definir cómo obtienes el valor de codigo_plantuml
    # Puedes recibirlo del cliente o generarlo con las tablas y columnas
    codigo_plantuml = generar_codigo_plantuml(tablas, columnas)  # Asegúrate de pasar los datos correctos
    imagen_url = obtener_imagen_plantuml(codigo_plantuml)
    return render(request, 'mostrar_diagrama.html', {'imagen_url': imagen_url})
