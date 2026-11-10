from django.db import models

from .base import ModeloBase


class TipoPropiedad(ModeloBase):
    """Catálogo: casa, departamento, terreno..."""
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'tipo de propiedad'
        verbose_name_plural = 'tipos de propiedad'

    def __str__(self):
        return self.nombre


class Caracteristica(ModeloBase):
    """Etiqueta: estacionamiento, bodega, terraza..."""
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'característica'

    def __str__(self):
        return self.nombre
