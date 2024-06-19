from django.urls import path
from .import views

urlpatterns = [
   path('', views.wishlist, name = 'wishlist'),
   path('add_to_list/<int:product_id>/', views.add_to_wishlist, name='add_to_list'),
   path('move_to_cart/<int:p_id>/', views.wishlist_to_cart, name = 'wishlist_to_cart')
   
]