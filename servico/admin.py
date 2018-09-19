from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Servico


@admin.register(Servico)
class ServicoAdmin(ImportExportModelAdmin):
    list_display = ('id','activo', 'codigo', 'zona', 'cliente', 'nome', 'valor_dia', 'portagens', 'fatura')
