from django.contrib import admin
from django.urls import include, path
from django.template.response import TemplateResponse


def redoc_view(request):
    return TemplateResponse(request, 'redoc.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('redoc/', redoc_view, name='redoc'),
]
