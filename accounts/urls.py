from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="products"),
    path('customer/<int:pk>', views.customer, name = "customer"),
    path('', views.home, name="home"),

    path('create_order/<int:pk>', views.createOrder, name = "create_order" ),
    path('update_order/<int:pk>', views.updateOrder, name = "update_order" ),
    path('remove_order/<int:pk>', views.removeOrder, name = "remove_order" ),

    path('create_customer/', views.createCustomer, name = "create_customer" ),
    path('update_customer/<int:pk>', views.updateCustomer, name = "update_customer" ),
    
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
]

