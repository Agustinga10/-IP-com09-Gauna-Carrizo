# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    # 1) traer un listado de imágenes crudas desde la API
    raw_images = transport.getAllImages()
    
    # 2) convertir cada img. en una card
    cards = []
    for raw_image in raw_images:
        card = translator.fromRequestIntoCard(raw_image)
        cards.append(card)
    
    # 3) retornar el listado de cards
    return cards

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []
    
    # Obtener todas las imágenes
    all_cards = getAllImages()
    
    # Filtrar por nombre (ignorando mayúsculas/minúsculas)
    for card in all_cards:
        if name.lower() in card.name.lower():
            filtered_cards.append(card)
    
    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []
    
    # Obtener todas las imágenes
    all_cards = getAllImages()
    
    # Filtrar por tipo
    for card in all_cards:
        # Verificar si el tipo está en la lista de tipos del Pokémon
        for type in card.types:
            if type_filter.lower() == type.lower():
                filtered_cards.append(card)
    
    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    # Crear una nueva card con los datos del request
    fav = translator.fromTemplateIntoCard(request)
    # Asignar el usuario actual
    fav.user = get_user(request)
    # Guardar en la base de datos
    return repositories.save_favourite(fav)

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        # Obtener favoritos del usuario desde la base de datos
        favourite_list = repositories.get_all_favourites(user)
        mapped_favourites = []
        
        # Convertir cada favorito en una Card
        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite)
            mapped_favourites.append(card)
        
        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId)

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)

def deleteAllFavourites(request):
    # Eliminar todos los favoritos del usuario
    repositories.delete_all_favourites(request.user)