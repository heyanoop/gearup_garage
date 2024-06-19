from django.urls import path
from .import views

urlpatterns = [
    path('', views.store,name = 'store'),
    path('category/<slug:category_slug>/', views.store, name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name = 'product_details'),
    path('product_search/',views.product_search, name ='product_search'),
    path('price_range', views.price_range, name = 'price_range'),
    path('get_variant_stock/<int:variation_id>/', views.get_variant_stock, name='get_variant_stock'),
    
]