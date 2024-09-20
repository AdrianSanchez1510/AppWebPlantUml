from django.urls import path
from . import views

urlpatterns = [
    path('generar-diagrama/', views.generar_diagrama, name='generar_diagrama'),
]
