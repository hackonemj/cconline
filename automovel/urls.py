from django.urls import path

from .views import automovel

app_name = 'automovel'

urlpatterns = [
    path('', automovel, name='lista'),
]
