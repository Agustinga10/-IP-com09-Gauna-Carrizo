# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    # Obtener todas las imágenes de Pokémon
    images = services.getAllImages()
    
    # Obtener favoritos si el usuario está autenticado
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        # Obtener imágenes filtradas por nombre
        images = services.filterByCharacter(name)
        
        # Obtener favoritos si el usuario está autenticado
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        # Obtener imágenes filtradas por tipo
        images = services.filterByType(type)
        
        # Obtener favoritos si el usuario está autenticado
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services.getAllFavourites(request)

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Obtener todos los favoritos del usuario
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    # Guardar un nuevo favorito
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    # Eliminar un favorito
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Las contraseñas no coinciden'})

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'El nombre de usuario ya existe'})

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Iniciar sesión automáticamente
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        
        # Verificar la contraseña
        if authenticate(username=user.username, password=password):
            # Eliminar todos los favoritos del usuario
            services.deleteAllFavourites(request)
            
            # Eliminar el usuario
            user.delete()
            
            # Cerrar la sesión
            logout(request)
            
            return redirect('index-page')
        else:
            return render(request, 'delete_account.html', {
                'error_message': 'La contraseña es incorrecta'
            })
    
    return render(request, 'delete_account.html')