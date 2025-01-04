

# Aplicaciones/Libros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.libros_list, name='libros_list'),
    path('libro/<int:pk>/', views.libro_detalle, name='libro_detalle'),
    path('agregar/', views.agregar_libro, name='agregar_libro'),
    path('libro/<int:pk>/editar/', views.editar_libro, name='editar_libro'),
    path('libro/<int:pk>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    path('libro/<int:pk>/comprar/', views.comprar_libro, name='comprar_libro'),
   
]