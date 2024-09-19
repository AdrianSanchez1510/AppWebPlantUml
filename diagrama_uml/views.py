from django.shortcuts import render
from .services import generar_codigo_plantuml, obtener_imagen_plantuml

# views.py
from django.shortcuts import render, redirect

def mostrar_diagrama(request):
    codigo_plantuml = generar_codigo_plantuml(tablas, columnas)
    imagen_url = obtener_imagen_plantuml(codigo_plantuml)
    return render(request, 'mostrar_diagrama.html', {'imagen_url': imagen_url})

def conectar_base(request):
    # Lógica para conectar a la base de datos
    return redirect('mostrar_diagrama')  # Redirige después de conectar

def actualizar_uml(request):
    # Lógica para actualizar el UML
    return redirect('mostrar_diagrama')  # Redirige después de actualizar
