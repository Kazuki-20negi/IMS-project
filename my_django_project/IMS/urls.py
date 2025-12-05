from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # 変更前: path('health/<int:page_id>/', views.health, name='health')
    # 変更後: どのページにも対応できる汎用的なURLに変更
    path('page/<int:page_id>/', views.page_detail, name='page_detail'),
]