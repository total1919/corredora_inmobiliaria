from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from publicidad.models import TipoPropiedad, Caracteristica, Propiedad, Consulta

CLAVE = 'prueba1234'


class Command(BaseCommand):
    help = 'Carga los datos de prueba mínimos del caso.'

    def handle(self, *args, **options):
        # 3 usuarios
        usuarios = {}
        for username, nombre in [('ana', 'Ana'), ('bruno', 'Bruno'), ('carla', 'Carla')]:
            user, creado = User.objects.get_or_create(
                username=username,
                defaults={'first_name': nombre, 'email': f'{username}@correo.cl'},
            )
            if creado:
                user.set_password(CLAVE)
                user.save()
            usuarios[username] = user

        # 3 tipos de propiedad
        tipos = {}
        for nombre in ['Casa', 'Departamento', 'Terreno']:
            tipos[nombre], _ = TipoPropiedad.objects.get_or_create(nombre=nombre)

        # 5 características
        caracteristicas = {}
        for nombre in ['Estacionamiento', 'Bodega', 'Terraza', 'Piscina', 'Jardín']:
            caracteristicas[nombre], _ = Caracteristica.objects.get_or_create(nombre=nombre)

        # 10 propiedades: (título, precio, m², estado, tipo, dueño, características)
        datos = [
            ('Casa amplia en El Palomar', 120000000, 180, 'disponible', 'Casa', 'ana', ['Estacionamiento', 'Jardín', 'Piscina']),
            ('Departamento céntrico', 65000000, 60, 'disponible', 'Departamento', 'ana', ['Terraza', 'Bodega']),
            ('Terreno en Hacienda San Pedro', 30000000, 500, 'disponible', 'Terreno', 'ana', []),
            ('Casa familiar en Rosario', 95000000, 140, 'reservada', 'Casa', 'bruno', ['Estacionamiento', 'Jardín']),
            ('Departamento con vista', 72000000, 75, 'disponible', 'Departamento', 'bruno', ['Terraza', 'Estacionamiento']),
            ('Parcela en Tierra Amarilla', 45000000, 5000, 'vendida', 'Terreno', 'bruno', []),
            ('Casa con quincho', 110000000, 160, 'disponible', 'Casa', 'carla', ['Piscina', 'Estacionamiento', 'Bodega']),
            ('Departamento para estudiantes', 48000000, 40, 'disponible', 'Departamento', 'carla', ['Bodega']),
            ('Sitio esquina', 38000000, 300, 'reservada', 'Terreno', 'carla', []),
            ('Oficina habilitada como vivienda', 55000000, 70, 'disponible', None, 'carla', ['Estacionamiento']),
        ]
        propiedades = []
        for titulo, precio, m2, estado, tipo, dueno, caracts in datos:
            propiedad, creado = Propiedad.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'descripcion': f'{titulo}. Propiedad de prueba en Copiapó y alrededores.',
                    'precio': precio,
                    'metros_cuadrados': m2,
                    'estado': estado,
                    'tipo': tipos.get(tipo),
                    'corredor': usuarios[dueno],
                },
            )
            if creado:
                propiedad.caracteristicas.set([caracteristicas[c] for c in caracts])
            propiedades.append(propiedad)

        # 5 consultas en distintos estados (siempre sobre propiedades ajenas)
        consultas = [
            (propiedades[3], 'ana', '¿Se puede visitar el sábado?', '', 'nueva'),
            (propiedades[0], 'bruno', '¿Acepta crédito hipotecario?', 'Sí, sin problema.', 'respondida'),
            (propiedades[6], 'ana', '¿La piscina es temperada?', 'No, es normal.', 'cerrada'),
            (propiedades[1], 'carla', '¿Tiene gastos comunes altos?', '', 'cancelada'),
            (propiedades[4], 'carla', '¿Hasta cuándo está disponible?', '', 'nueva'),
        ]
        for propiedad, usuario, mensaje, respuesta, estado in consultas:
            Consulta.objects.get_or_create(
                propiedad=propiedad,
                interesado=usuarios[usuario],
                mensaje=mensaje,
                defaults={'respuesta': respuesta, 'estado': estado},
            )

        self.stdout.write(self.style.SUCCESS(
            f'Datos cargados. Usuarios: ana, bruno, carla (clave: {CLAVE}).'
        ))
