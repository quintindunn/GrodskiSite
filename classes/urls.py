from django.urls import path
from .views import view_subject, new_page, new_category

urlpatterns = [
    path('<str:pk_dynamic>/', view_subject, name="site-subject-dynamic"),
    path('new/page', new_page, name="new-page"),
    path('new/category', new_category, name="new-category")
]
