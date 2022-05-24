from django.urls import path, include
from . import views


app_name = 'board'

urlpatterns = [
    path('new/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]