from django.db import models

class ConexionBD(models.Model):
    tipo_base_datos = models.CharField(max_length=50)
    host = models.CharField(max_length=100)
    puerto = models.CharField(max_length=10)
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    nombre_base_datos = models.CharField(max_length=100)
