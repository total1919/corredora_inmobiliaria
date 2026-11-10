from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from .base import ModeloBase
from .catalogo import TipoPropiedad, Caracteristica

ESTADOS_PROPIEDAD = ['disponible', 'reservada', 'vendida']


class Propiedad(ModeloBase):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    metros_cuadrados = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=20, default='disponible')

    corredor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propiedades')

    # Requisito 12: si se elimina un tipo, la propiedad NO se borra;
    # queda sin tipo, porque el caso dice que el catálogo es opcional.
    tipo = models.ForeignKey(
        TipoPropiedad, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='propiedades',
    )
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True, related_name='propiedades')

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.titulo
