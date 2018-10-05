from django.urls import path

from .views import automovel_with_jquery

app_name = 'automovel'

urlpatterns = [
    path('', automovel_with_jquery, name='lista'),
]
