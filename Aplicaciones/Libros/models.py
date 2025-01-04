from django.db import models
from django.contrib.auth.models import User

# Modelo para Libro
class Libro(models.Model):
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    imagen = models.ImageField(upload_to='libros_imagenes/', blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


# Modelo para Compra
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que realiza la compra
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)  # Libro comprado
    fecha_compra = models.DateTimeField(auto_now_add=True)  # Fecha en que se realizó la compra
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de libros comprados
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total de la compra

    def __str__(self):
        return f"Compra de {self.usuario.username} - {self.libro.titulo}"
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS, default='comprador')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"
