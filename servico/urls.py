from django.urls import path

from .views import servico, index

app_name = 'servico'

urlpatterns = [
    # path('', servico, name='lista'),
    path('', index, name='lista'),
]
