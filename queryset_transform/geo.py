from django.contrib.gis.db.models.manager import GeoManager
from django.contrib.gis.db.models.query import GeoQuerySet

from . import TransformQuerySetMixin


class GeoTransformQuerySet(TransformQuerySetMixin, GeoQuerySet):
    pass


class GeoTransformManager(GeoManager):
    def get_queryset(self):
        return GeoTransformQuerySet(self.model)
