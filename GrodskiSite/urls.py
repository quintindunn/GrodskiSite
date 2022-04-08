from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include("files.urls")),
    path('api/', include("api.urls")),
    path('admin/', admin.site.urls),
    path('', include('home_page.urls')),
    path('', include('classes.urls')),
    path('urls/', include("core.urls"))
]
