# models.py
from django.contrib.gis.db import models

class RouteNationale(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    osm_id = models.CharField(max_length=255, null=True)
    code = models.IntegerField(null=True)
    fclass = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    ref = models.CharField(max_length=255, null=True)
    oneway = models.CharField(max_length=255, null=True)
    maxspeed = models.IntegerField(null=True)
    layer = models.FloatField(null=True)
    bridge = models.CharField(max_length=255, null=True)
    tunnel = models.CharField(max_length=255, null=True)
    geom = models.MultiLineStringField(srid=4326)
    longueur_km = models.FloatField(null=True, blank=True)
    etat = models.CharField(max_length=50, null=True)

    class Meta:
        managed = False
        db_table = 'routes_nationales'

    def __str__(self):
        return self.name or self.ref or str(self.ogc_fid)