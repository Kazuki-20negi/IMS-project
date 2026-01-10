from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_audiogram, name='upload_audiogram'),
]