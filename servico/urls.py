from django.urls import path

from .views import servico

app_name = 'servico'

urlpatterns = [
    path('', servico, name='lista'),
]
