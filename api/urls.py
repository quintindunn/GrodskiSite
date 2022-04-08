from django.urls import path
from .views import new_page

urlpatterns = [
    path('newpage', new_page, name="new-page"),
]
