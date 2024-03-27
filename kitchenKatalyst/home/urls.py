from django.urls import path
from . import views

#include paths to views here
urlpatterns = [

    path('', views.index, name='index'),
    path('create_account/', views.create_account, name='create_account'),
    path('main/', views.main, name='main'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('recipe/', views.recipe, name='recipe'), 
    path('admin_welcome/', views.admin_welcome, name='admin_welcome'),
    path('logout/', views.logout, name='logout'),
    path('delete/<int:grocery_number>', views.delete, name="delete"),

   
]