from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Consulta, ESTADOS_ABIERTOS


# ---------- Lado del interesado ----------

@login_required
def mis_consultas(request):
    consultas = (
        Consulta.objects
        .filter(interesado=request.user)
        .select_related('propiedad')
    )
    return render(request, 'mis_consultas.html', {'consultas': consultas})


@login_required
def consulta_cancelar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if consulta.interesado != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        if consulta.estado == 'nueva':
            consulta.estado = 'cancelada'
            consulta.save()
            messages.success(request, 'Consulta cancelada.')
        else:
            messages.error(request, 'Solo puedes cancelar consultas nuevas.')

    return redirect('mis_consultas')


# ---------- Lado del corredor (dueño de la propiedad) ----------

def obtener_recibida(request, pk):
    """Busca la consulta; si la propiedad no es del usuario, responde 'sin permiso'."""
    consulta = get_object_or_404(Consulta.objects.select_related('propiedad'), pk=pk)
    if consulta.propiedad.corredor != request.user:
        raise PermissionDenied
    return consulta


@login_required
def consultas_recibidas(request):
    consultas = (
        Consulta.objects
        .filter(propiedad__corredor=request.user)
        .select_related('propiedad', 'interesado')
    )
    return render(request, 'consultas_recibidas.html', {'consultas': consultas})


@login_required
def consulta_responder(request, pk):
    consulta = obtener_recibida(request, pk)
    respuesta = request.POST.get('respuesta', '').strip()

    if request.method == 'POST' and consulta.estado in ESTADOS_ABIERTOS:
        if respuesta:
            consulta.respuesta = respuesta
            consulta.estado = 'respondida'
            consulta.save()
            messages.success(request, 'Respuesta enviada.')
        else:
            messages.error(request, 'Escribe una respuesta antes de enviar.')

    return redirect('consultas_recibidas')


@login_required
def consulta_cerrar(request, pk):
    consulta = obtener_recibida(request, pk)

    if request.method == 'POST' and consulta.estado in ESTADOS_ABIERTOS:
        consulta.estado = 'cerrada'
        consulta.save()
        messages.success(request, 'Consulta cerrada.')

    return redirect('consultas_recibidas')
