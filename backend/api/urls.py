# backend/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('analyze/', views.analyze_query, name='analyze'),
    path('health/', views.health_check, name='health'),
]