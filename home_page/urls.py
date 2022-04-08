from django.urls import path
from home_page.views import index
urlpatterns = [
    path('', index, name='site-home')
]
