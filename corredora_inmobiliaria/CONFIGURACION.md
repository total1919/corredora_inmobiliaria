# Configuración que va fuera de la app `publicidad`

## urls.py del proyecto

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),  # login, logout, password_change
    path('', include('publicidad.urls')),
]
```

## settings.py

```python
INSTALLED_APPS = [
    # ... las de Django ...
    'publicidad',
]

TEMPLATES = [
    {
        # ...
        'DIRS': [BASE_DIR / 'templates'],   # carpeta templates/ en la raíz
        # ...
    },
]

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'portada'
LOGOUT_REDIRECT_URL = 'portada'
```

## Pasos para levantarlo de cero

1. Reemplazar las carpetas `models/`, `forms/`, `views/` y `templates/` completas (para que no queden archivos viejos), borrar `models.py` si existe y los archivos de
   `publicidad/migrations/` excepto `__init__.py`.
2. Borrar y volver a crear la base en MySQL.
3. Ejecutar:

```
python manage.py makemigrations publicidad
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_datos
python manage.py runserver
```

## Para ver la página "Sin permiso" (403.html)

Django solo usa `templates/403.html` cuando `DEBUG = False`.
Con `DEBUG = True` igual bloquea, pero muestra su página genérica "403 Forbidden".
