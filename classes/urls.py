from django.urls import path
from .views import view_subject, new_page, new_category, new_class, change_background

urlpatterns = [
    path('<str:pk_dynamic>/', view_subject, name="site-subject-dynamic"),
    path('new/page', new_page, name="new-page"),
    path('new/category', new_category, name="new-category"),
    path('new/class', new_class, name="new-class"),
    path('new/background', change_background, name="change-background")
]
