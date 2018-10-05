from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from automovel.views import AutomovelViewSet
from servico.views import ServicoViewSet

router = DefaultRouter()
router.register(r'servico', ServicoViewSet)
router.register(r'automovel', AutomovelViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('core.urls')),
                  path('conta/', include('conta.urls')),
                  path('recurso-humano/', include('recurso_humano.urls')),
                  path('servico/', include('servico.urls')),
                  path('automovel/', include('automovel.urls')),
                  path('conta/', include('django.contrib.auth.urls')),
                  path('api/', include(router.urls)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
