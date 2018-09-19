from django.contrib import admin
from .models import RecursoHumano
from import_export.admin import ImportExportModelAdmin


@admin.register(RecursoHumano)
class RecusoHumanoAdmin(ImportExportModelAdmin):
    list_display = ('activo', 'nif', 'id_funcionario', 'nome_completo', 'nome', 'obs')
