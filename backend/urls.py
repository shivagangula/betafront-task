from django.contrib import admin
from django.urls import path, include
from pokemon.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/pokemon/', include('pokemon.urls')),
    path('', homepage, name='homepage'),
    
]
