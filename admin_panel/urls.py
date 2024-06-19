from django.urls import path
from .import views

urlpatterns = [
    path('', views.admin_login, name  = 'admin_login'),
    path('admin_dash/', views.admin_dashboard, name = 'admin_dash'),
    path('user_list/', views.user_list, name = 'user_list'),
    path('product_list/', views.product_list, name = 'product_list'),
    path('category_list/', views.category_list, name = 'category_list'),
    path('edit_user/<int:user_id>/', views.user_edit, name = 'edit_user'),
    path('edit_product/<int:product_id>/', views.edit_product, name = 'edit_product'),
    path('edit_category/<int:category_id>/', views.edit_category, name = 'edit_category'),
    path('add_product/', views.add_product, name = 'add_product'),
    path('add_category/', views.add_category, name = 'add_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('add_user/', views.add_user, name = 'add_user'),
    path('product/<int:product_id>/toggle/', views.toggle_product_active, name='toggle_product_active'),
    path('orders/', views.orders, name = 'orders'),
    path('order_details/<int:order_id>/',views.order_details, name = 'order_details'),
    # path('deactivate_user/<int:user_id>/', views.deactivate_user, name = 'deactivate_user'),
    # path('activate_user/<int:user_id>/', views.activate_user, name = 'activate_user'),
    path('toggle_user/<int:user_id>/', views.toggle_user_activation, name='toggle_user_activation'),
    path('update_status/<int:status_id>', views.update_order_status, name = 'update_order'),
    path('coupon/', views.coupon_manager, name = 'coupon'),
    path('add_coupon', views.add_coupon, name = 'add_coupon'),
    path('coupons/<int:coupon_id>/toggle-active/', views.toggle_coupon_active, name='toggle_coupon_active'),
    path('sales_report', views.sales_report, name = 'sales_report'),
    path('category_offer', views.cat_offer, name = 'category_offer'),
    path('product_offer', views.prod_offer, name = 'product_offer'),
    path('add_product_offer', views.add_product_offer, name = 'add_product_offer'),
    path('add_category_offer', views.add_category_offer, name = 'add_category_offer'),
    path('delete_category_offer/<int:offer_id>/', views.delete_category_offer, name='delete_category_offer'),
    path('delete_product_offer/<int:offer_id>/', views.delete_product_offer, name='delete_product_offer'),
    path('approve_return/<int:id>/',views.approve_return, name = 'approve_return' ),
    path('reject_return/<int:id>/',views.reject_return, name = 'reject_return'),
    path('init_refund/<int:id>/',views.init_refund, name = 'init_refund' )    
    
]