from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import RegistroForm, CuentaForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('portada')

    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Cuenta creada. ¡Bienvenido!')
        return redirect('portada')

    return render(request, 'registro.html', {'form': form})


@login_required
def mi_cuenta(request):
    form = CuentaForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Datos actualizados.')
        return redirect('mi_cuenta')

    return render(request, 'mi_cuenta.html', {'form': form})
