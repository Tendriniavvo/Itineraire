# views.py
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from .models import RouteNationale
VITESSES = {
    'primary': {'bon': 60, 'moyen': 40, 'mauvais': 20},
    'secondary': {'bon': 40, 'moyen': 30, 'mauvais': 10},
    'tertiary': {'bon': 20, 'moyen': 15, 'mauvais': 5},
}


def geojson_routes(request):
    """Vue qui retourne les données GeoJSON avec longueurs et durées totales par RN"""

    def get_vitesse(fclass, etat):
        fclass = (fclass or 'secondary').lower()
        etat = (etat or 'moyen').lower()
        return VITESSES.get(fclass, VITESSES['secondary']).get(etat, 40)

    routes_groupées = {}
    for route in RouteNationale.objects.all():
        ref = route.ref or f"(ID {route.ogc_fid})"
        if ref not in routes_groupées:
            routes_groupées[ref] = []
        routes_groupées[ref].append(route)

    features = []
    for ref, segments in routes_groupées.items():
        total_km = 0
        total_min = 0

        for seg in segments:
            longueur = seg.longueur_km or 0
            vitesse = get_vitesse(seg.fclass, seg.etat)
            duree = (longueur / vitesse) * 60 if vitesse > 0 else 0
            total_km += longueur
            total_min += duree

        # conversion en heures + minutes
        heures_totales = int(total_min // 60)
        minutes_restantes = int(total_min % 60)
        duree_hm = f"{heures_totales}h{minutes_restantes:02d}"

        for seg in segments:
            longueur_segment = seg.longueur_km or 0
            vitesse = get_vitesse(seg.fclass, seg.etat)
            duree_segment = (longueur_segment / vitesse) * 60 if vitesse > 0 else 0

            features.append({
                "type": "Feature",
                "geometry": json.loads(seg.geom.geojson),
                "properties": {
                    "name": seg.name,
                    "ref": seg.ref,
                    "fclass": seg.fclass,
                    "etat": seg.etat,
                    "longueur_segment_km": round(longueur_segment, 2),
                    "longueur_totale_km": round(total_km, 2),
                    "duree_estimee_min": round(duree_segment, 1),
                    "duree_totale_min": round(total_min, 1),
                    "duree_totale_formatee": duree_hm
                }
            })

    return JsonResponse({
        "type": "FeatureCollection",
        "features": features,
    })




def carte(request):
    """Vue qui affiche la page HTML avec la carte"""
    return render(request, "carto/carte.html")