from django.urls import path
from . import views

urlpatterns = [
    path('', views.carte, name='carte'),  # Page principale avec la carte
    path('routes/', views.geojson_routes, name='geojson_routes'),  # Données JSON
]