from django.contrib import admin
from .models import ServicoDiario, CO


@admin.register(ServicoDiario)
class ServicoDiarioAdmin(admin.ModelAdmin):
    list_display = (
        'id','co', 'automovel', 'condutor', 'servico', 'km_inicial', 'km_final', 'estado_concluido', 'supervisor', 'validar_servico'
    )
    list_filter = ('created_at', 'update_at')


admin.site.register(CO)