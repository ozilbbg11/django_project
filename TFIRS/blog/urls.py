from django.urls import path
from .views import search_list, recipe_detail
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('trend/', views.trend, name='blog-trend'),
    path('generate/', views.generate, name='blog-generate'),
    path('search/', search_list, name='blog-search-list'),
    path('recipe/<slug>', recipe_detail, name='blog-recipe-detail'),
]