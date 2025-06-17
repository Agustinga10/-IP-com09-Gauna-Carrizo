# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages(name=None, type_filter=None):
    json_collection = transport.getAllImages()
    images = []

    for item in json_collection:
        if 'image' in item:
            card = translator.fromRequestIntoCard(item)
            if name and name.lower() not in card.name.lower():
                continue
            if type_filter and card.type.lower() != type_filter.lower():
                continue
            images.append(card)
    return images
# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon.
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    pass

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    return getAllImages(name=name)



# función que filtra las cards según su tipo.
def filterByType(type_filter):
    return getAllImages(type_filter=type_filter)

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        favourite_list = repositories.get_all_favourites(user)
        mapped_favourites = []
        for fav in favourite_list:
            card = translator.fromRepositoryIntoCard(fav)
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)