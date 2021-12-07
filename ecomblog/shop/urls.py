from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
urlpatterns = [
    path('', views.index,name="shopHome"),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path('tracker/', views.tracker,name="tracker"),
    path('search/', views.search,name="search"),
    path('products/<int:myid>', views.productview,name="productview"),
    path('checkout/', views.checkout,name="checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('cart/', views.cart,name="cart"),
    path('login/', views.login,name="login"),
    path('signup/', views.signup,name="signup"),
]