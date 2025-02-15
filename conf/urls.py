from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .api import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('',
        TemplateView.as_view(template_name='index.html'),
        name='app',
    ),
]
