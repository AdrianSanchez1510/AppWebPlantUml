from django.http import HttpResponse
from .services import generar_diagrama_para_base_datos

def generar_diagrama(request):
    # Parámetros de conexión obtenidos desde la URL o formulario
    tipo_base_datos = request.GET.get('tipo_base_datos', 'postgresql')
    host = request.GET.get('host', 'localhost')
    puerto = int(request.GET.get('puerto', 5432))
    usuario = request.GET.get('usuario', 'admin')
    password = request.GET.get('password', 'admin')
    nombre_base_datos = request.GET.get('nombre_base_datos', 'Practica')

    # Generar el diagrama
    imagen_binaria = generar_diagrama_para_base_datos(tipo_base_datos, host, puerto, usuario, password, nombre_base_datos)
    
    if imagen_binaria:
        return HttpResponse(imagen_binaria, content_type="image/png")
    else:
        return HttpResponse("No se pudo generar el diagrama.", status=400)
