from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import PropiedadForm, TipoPropiedadForm
from ..models import Propiedad


def obtener_propia(request, pk):
    """Busca la propiedad; si no es del usuario, responde 'sin permiso' (403)."""
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if propiedad.corredor != request.user:
        raise PermissionDenied
    return propiedad


@login_required
def mis_propiedades(request):
    propiedades = (
        Propiedad.objects
        .filter(corredor=request.user)
        .select_related('tipo')
    )
    return render(request, 'mis_propiedades.html', {'propiedades': propiedades})


@login_required
def propiedad_crear(request):
    form = PropiedadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        propiedad = form.save(commit=False)
        propiedad.corredor = request.user
        propiedad.save()
        form.save_m2m()
        messages.success(request, 'Propiedad publicada.')
        return redirect('propiedad_detalle', pk=propiedad.pk)

    return render(request, 'propiedad_form.html', {'form': form})


@login_required
def propiedad_editar(request, pk):
    propiedad = obtener_propia(request, pk)

    form = PropiedadForm(request.POST or None, instance=propiedad)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Propiedad actualizada.')
        return redirect('propiedad_detalle', pk=propiedad.pk)

    return render(request, 'propiedad_form.html', {'form': form, 'propiedad': propiedad})


@login_required
def propiedad_eliminar(request, pk):
    propiedad = obtener_propia(request, pk)

    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'Propiedad eliminada.')
        return redirect('mis_propiedades')

    return render(request, 'propiedad_eliminar.html', {'propiedad': propiedad})


@login_required
def tipo_crear(request):
    form = TipoPropiedadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tipo = form.save()
        messages.success(request, f'Tipo "{tipo}" creado. Ya puedes elegirlo.')
        return redirect('propiedad_crear')

    return render(request, 'tipo_form.html', {'form': form})
