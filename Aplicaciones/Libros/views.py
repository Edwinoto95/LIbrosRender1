from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Libro
from .forms import LibroForm
from .models import Libro, Compra  # Importamos el modelo Compra

def libros_list(request):
    query = request.GET.get('q', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    
    # Filtrar por búsqueda por título
    libros = Libro.objects.all()
    
    if query:
        libros = libros.filter(titulo__icontains=query, disponible=True)
    if precio_min:
        libros = libros.filter(precio__gte=precio_min)
    if precio_max:
        libros = libros.filter(precio__lte=precio_max)
    libros = libros.filter(disponible=True)

    return render(request, 'libros_list.html', {
        'libros': libros, 
        'query': query,
        'precio_min': precio_min,
        'precio_max': precio_max
    })

def libro_detalle(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'libro_detalle.html', {'libro': libro})

@login_required
def agregar_libro(request, pk=None):
    if pk:
        libro = get_object_or_404(Libro, pk=pk)
    else:
        libro = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.vendedor = request.user
            libro.save()
            messages.success(request, 'Libro agregado/editado exitosamente.')
            return redirect('libros_list')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'agregar_libro.html', {'form': form, 'libro': libro})

@login_required
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    
    # Verifica que el usuario sea el vendedor del libro
    if libro.vendedor != request.user:
        messages.error(request, 'No tienes permiso para editar este libro.')
        return redirect('libro_detalle', pk=libro.pk)

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado exitosamente.')
            return redirect('libro_detalle', pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'editar_libro.html', {'form': form, 'libro': libro})

@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    # Verifica que el usuario sea el vendedor del libro
    if libro.vendedor != request.user:
        messages.error(request, 'No tienes permiso para eliminar este libro.')
        return redirect('libro_detalle', pk=libro.pk)

    libro.delete()  # Elimina el libro de la base de datos
    messages.success(request, 'Libro eliminado exitosamente.')
    return redirect('libros_list')  # Redirige a la lista de libros




@login_required
def comprar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    # Verificamos si el libro está disponible para compra
    if not libro.disponible:
        messages.error(request, 'Este libro ya no está disponible para compra.')
        return redirect('libros_list')

    # Crear una nueva compra
    compra = Compra.objects.create(libro=libro, usuario=request.user)
    
    # Actualizar la disponibilidad del libro, marcándolo como no disponible
    libro.disponible = False
    libro.save()

    # Mensaje de éxito
    messages.success(request, f'¡Has comprado el libro "{libro.titulo}" exitosamente!')

    # Redirigir a la lista de libros
    return redirect('libros_list')







