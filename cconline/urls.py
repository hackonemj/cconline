from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('core.urls')),
                  path('conta/', include('conta.urls')),
                  path('recurso-humano/', include('recurso_humano.urls')),
                  path('servico/', include('servico.urls')),
                  path('automovel/', include('automovel.urls')),
                  path('conta/', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
