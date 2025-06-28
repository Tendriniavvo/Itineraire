# views.py
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from .models import RouteNationale


def geojson_routes(request):
    """Vue qui retourne les données GeoJSON avec longueurs totales"""

    # Calculer les longueurs totales par référence de route
    longueurs_totales = {}
    routes_avec_ref = RouteNationale.objects.filter(
        ref__isnull=False
    ).values('ref').annotate(
        longueur_totale=Sum('longueur_km')
    )

    for route_data in routes_avec_ref:
        ref = route_data['ref']
        longueur_totale = round(route_data['longueur_totale'], 2)
        longueurs_totales[ref] = longueur_totale

    # Générer les features GeoJSON
    features = []
    for route in RouteNationale.objects.all():
        # Récupérer la longueur totale de la route ou du segment
        if route.ref and route.ref in longueurs_totales:
            longueur_totale = longueurs_totales[route.ref]
        else:
            longueur_totale = route.longueur_km or 0

        features.append({
            "type": "Feature",
            "geometry": json.loads(route.geom.geojson),
            "properties": {
                "name": route.name,
                "ref": route.ref,
                "fclass": route.fclass,
                "longueur_segment_km": route.longueur_km or 0,
                "longueur_totale_km": longueur_totale
            }
        })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features,
    })


def carte(request):
    """Vue qui affiche la page HTML avec la carte"""
    return render(request, "carto/carte.html")