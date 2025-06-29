from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<int:id>/', views.pokemon_detail, name='pokemon-detail'),
    path('', views.index_page, name='index-page'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='registro'),
    path('home/', views.home, name='home'),
    
    path('buscar/', views.search, name='buscar'),
    path('filter_by_type/', views.filter_by_type, name='filter_by_type'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', views.exit, name='exit'),
    path('delete-account/', views.delete_account, name='delete-account'),
]