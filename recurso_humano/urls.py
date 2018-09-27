from django.urls import path

from .views import recurso_humano

app_name = 'recurso-humano'

urlpatterns = [
    path('', recurso_humano, name='lista'),
]