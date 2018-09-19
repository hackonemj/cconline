from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ajax/validate-codigo-servico/', views.validate_codigo_servico, name='validate_codigo_servico'),
    path('ajax/validate-automovel-matricula/', views.validate_automovel_matricula, name='validate_automovel_matricula'),
    path('ajax/finalizar-servico/<id>/', views.ajax_finalizar_servico, name='ajax_finalizar_servico'),

]
