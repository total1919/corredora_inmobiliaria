from django import forms

from ..models import Consulta, ESTADOS_ABIERTOS


class ConsultaForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = ['mensaje']
        labels = {'mensaje': 'Tu consulta'}
        widgets = {'mensaje': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, propiedad=None, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.propiedad = propiedad
        self.usuario = usuario

    # Reglas del caso para crear una consulta (requisito 13).
    def clean(self):
        datos = super().clean()

        if self.propiedad.corredor == self.usuario:
            raise forms.ValidationError('No puedes consultar por tu propia propiedad.')

        if self.propiedad.estado == 'vendida':
            raise forms.ValidationError('Esta propiedad ya fue vendida.')

        abierta = Consulta.objects.filter(
            propiedad=self.propiedad,
            interesado=self.usuario,
            estado__in=ESTADOS_ABIERTOS,
        )
        if abierta.exists():
            raise forms.ValidationError('Ya tienes una consulta abierta sobre esta propiedad.')

        return datos
