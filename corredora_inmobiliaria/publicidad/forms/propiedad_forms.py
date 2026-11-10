from django import forms

from ..models import Propiedad, TipoPropiedad, ESTADOS_PROPIEDAD

MAX_CARACTERISTICAS = 5


class PropiedadForm(forms.ModelForm):
    estado = forms.ChoiceField(
        choices=[(estado, estado.capitalize()) for estado in ESTADOS_PROPIEDAD],
    )

    class Meta:
        model = Propiedad
        fields = [
            'titulo', 'descripcion', 'precio', 'metros_cuadrados',
            'estado', 'tipo', 'caracteristicas',
        ]
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'metros_cuadrados': 'Metros cuadrados',
            'tipo': 'Tipo de propiedad',
            'caracteristicas': 'Características',
        }
        widgets = {
            'caracteristicas': forms.CheckboxSelectMultiple,
        }

    # Validación propia (requisito 9): hasta cinco características.
    def clean_caracteristicas(self):
        caracteristicas = self.cleaned_data['caracteristicas']
        if len(caracteristicas) > MAX_CARACTERISTICAS:
            raise forms.ValidationError(
                f'Elige como máximo {MAX_CARACTERISTICAS} características.'
            )
        return caracteristicas


class TipoPropiedadForm(forms.ModelForm):

    class Meta:
        model = TipoPropiedad
        fields = ['nombre']
