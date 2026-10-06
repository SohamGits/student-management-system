from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('greet/<str:name>/', views.greet, name='greet'),
    path('about/', views.about, name='about')
]