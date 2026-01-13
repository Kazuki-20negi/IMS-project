from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_audiogram, name='upload_audiogram'),
    path("", views.audiogram_list, name="audiograms"),
    path('edit/<int:audiogram_id>/', views.audiogram_edit, name='audiogram_edit'),
]