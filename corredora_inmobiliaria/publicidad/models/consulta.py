from django.contrib.auth.models import User
from django.db import models

from .base import ModeloBase
from .propiedad import Propiedad

ESTADOS_CONSULTA = ['nueva', 'respondida', 'cerrada', 'cancelada']
ESTADOS_ABIERTOS = ['nueva', 'respondida']


class Consulta(ModeloBase):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='consultas')
    interesado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    mensaje = models.TextField()
    respuesta = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default='nueva')

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'{self.interesado.username} → {self.propiedad} ({self.estado})'
