from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('api/', include("files.urls")),
    path('api/', include("api.urls")),
    path('admin/', admin.site.urls),
    path('', include('home_page.urls')),
    path('', include('classes.urls')),
    path('urls/', include("core.urls")),

]
