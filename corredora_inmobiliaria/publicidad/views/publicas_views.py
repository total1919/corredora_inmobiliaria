from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import ConsultaForm
from ..models import Propiedad, TipoPropiedad, Consulta


def portada(request):
    recientes = (
        Propiedad.objects
        .select_related('tipo', 'corredor')
        .order_by('-creado')[:4]
    )
    return render(request, 'portada.html', {
        'recientes': recientes,
        'total_disponibles': Propiedad.objects.filter(estado='disponible').count(),
        'total_tipos': TipoPropiedad.objects.count(),
        'total_consultas': Consulta.objects.count(),
    })


def propiedad_lista(request):
    q = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')

    propiedades = (
        Propiedad.objects
        .select_related('tipo', 'corredor')
        .prefetch_related('caracteristicas')
        .order_by('-creado')
    )

    if q:
        propiedades = propiedades.filter(
            Q(titulo__icontains=q) | Q(descripcion__icontains=q)
        )
    if tipo.isdigit():
        propiedades = propiedades.filter(tipo_id=tipo)

    paginator = Paginator(propiedades, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'propiedad_lista.html', {
        'propiedades': page_obj,
        'q': q,
        'tipos': TipoPropiedad.objects.all(),
        'tipo_id': tipo,
        'querystring': params.urlencode(),
    })


def propiedad_detalle(request, pk):
    propiedad = get_object_or_404(
        Propiedad.objects.select_related('tipo', 'corredor').prefetch_related('caracteristicas'),
        pk=pk,
    )

    puede_consultar = (
        request.user.is_authenticated
        and propiedad.corredor != request.user
        and propiedad.estado != 'vendida'
    )

    form = None
    if puede_consultar:
        form = ConsultaForm(request.POST or None, propiedad=propiedad, usuario=request.user)
        if request.method == 'POST' and form.is_valid():
            consulta = form.save(commit=False)
            consulta.propiedad = propiedad
            consulta.interesado = request.user
            consulta.save()
            messages.success(request, 'Consulta enviada.')
            return redirect('mis_consultas')

    elif request.method == 'POST' and not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'propiedad_detalle.html', {
        'propiedad': propiedad,
        'form': form,
    })
