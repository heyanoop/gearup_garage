from django.urls import path
from .import views
urlpatterns = [

    path('',views.cartitems,name="cart"),
    path('add_cart/<int:product_id>/', views.add_cart, name = 'add_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('remove_cart/<int:p_id>/', views.remove_cart, name = 'cart_remove'),
    path('add_address/', views.add_address, name = 'add_address'),
    path('cart_increase/<int:increase_id>/',views.cart_increase, name = 'cart_increase'),
    path('cart_decrease/<int:decrease_id>/',views.cart_decrease, name = 'cart_decrease'),
    path('apply_coupon', views.apply_coupon, name = 'apply_coupon'),
    path('remove_coupon', views.remove_coupon, name = 'remove_coupon')
]