import django_filters
from django.forms import DateInput

from servico.models import Servico
from servico_diario.models import ServicoDiario


class ServicoDiarioFilter(django_filters.FilterSet):
    servico = django_filters.ModelChoiceFilter(queryset=Servico.objects.all(), required=True)

    created_at = django_filters.DateFilter(
        widget=DateInput(attrs={'class': 'datepicker', 'placeholder': 'Data'}, format='%d/%m/%Y'), required=True
    )

    class Meta:
        model = ServicoDiario
        fields = ['servico', 'created_at']
        exclude = ['automovel', 'condutor', 'km_final', 'km_inicial', 'finished_at',
                   'validar_servico', 'supervisor', 'obs', 'estado_concluido', 'update_at', 'servico']
