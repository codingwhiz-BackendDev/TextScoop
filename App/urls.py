from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('extract', views.extract, name= 'extract'),
    path('view_file/<int:image_id>/', views.view_file, name='view_file'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]
