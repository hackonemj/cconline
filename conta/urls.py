from django.urls import path
from . import views

app_name = 'conta'

urlpatterns = [
    path('criar-conta/', views.criar_conta, name='criar-conta'),
    path('entrar/', views.entrar, name='entrar'),
    path('perfil/', views.ver_perfil, name='perfil'),
    path('sair/', views.sair, name='sair'),
]