from django.contrib import admin
from .models import Automovel
from import_export.admin import ImportExportModelAdmin


@admin.register(Automovel)
class AutomovelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'activo', 'dono', 'matricula', 'marca', 'modelo', 'data_matricula', 'km_actual')
    list_editable = ('data_matricula',)
