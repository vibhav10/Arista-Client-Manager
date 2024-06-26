"""
URL configuration for clientManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view 
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Arista Client Manager",
        default_version='v1',
        description="Welcome to Arista Client Manager API Documentation",
        terms_of_service="https://www.vibhav.servatom.com/",
        contact=openapi.Contact(email="vibhav.1507@gmail.com"),
        license=openapi.License(name="copright@2024"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def welcome(request):
    return HttpResponse("<H1 align=center> Welcome to client manager backend service </H1> <br> Please visit <a href= '/doc/'>/doc/</a> for API documentation")

urlpatterns = [
    path('', welcome),
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('manage/', include('clients.urls')),
    path('monitor/', include('monitor.urls')),
]
