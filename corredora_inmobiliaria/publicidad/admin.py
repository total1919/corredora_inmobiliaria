from django.contrib import admin

from .forms import PropiedadForm
from .models import TipoPropiedad, Caracteristica, Propiedad, Consulta


@admin.register(TipoPropiedad, Caracteristica)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creado')
    list_filter = ('creado',)
    search_fields = ('nombre',)


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    form = PropiedadForm
    list_display = ('titulo', 'precio', 'metros_cuadrados', 'estado', 'tipo', 'corredor', 'creado')
    list_filter = ('estado', 'tipo', 'caracteristicas')
    search_fields = ('titulo', 'descripcion')
    list_select_related = ('tipo', 'corredor')
    filter_horizontal = ('caracteristicas',)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('propiedad', 'interesado', 'estado', 'creado')
    list_filter = ('estado', 'creado')
    search_fields = ('propiedad__titulo', 'interesado__username', 'mensaje')
    list_select_related = ('propiedad', 'interesado')
