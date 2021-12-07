from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
urlpatterns = [
    path('', views.index,name="blogHome"),
    path('blogpost/<int:id>', views.blogpost,name="blogHome"),
]