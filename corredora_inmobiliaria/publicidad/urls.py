from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.portada, name='portada'),
    path('propiedades/', views.propiedad_lista, name='propiedad_lista'),
    path('propiedades/<int:pk>/', views.propiedad_detalle, name='propiedad_detalle'),

    # Cuentas
    path('registro/', views.registro, name='registro'),
    path('cuenta/', views.mi_cuenta, name='mi_cuenta'),

    # CRUD de propiedades
    path('mis-propiedades/', views.mis_propiedades, name='mis_propiedades'),
    path('propiedades/nueva/', views.propiedad_crear, name='propiedad_crear'),
    path('propiedades/<int:pk>/editar/', views.propiedad_editar, name='propiedad_editar'),
    path('propiedades/<int:pk>/eliminar/', views.propiedad_eliminar, name='propiedad_eliminar'),
    path('tipos/nuevo/', views.tipo_crear, name='tipo_crear'),

    # Consultas
    path('mis-consultas/', views.mis_consultas, name='mis_consultas'),
    path('consultas/<int:pk>/cancelar/', views.consulta_cancelar, name='consulta_cancelar'),
    path('consultas-recibidas/', views.consultas_recibidas, name='consultas_recibidas'),
    path('consultas/<int:pk>/responder/', views.consulta_responder, name='consulta_responder'),
    path('consultas/<int:pk>/cerrar/', views.consulta_cerrar, name='consulta_cerrar'),
]
