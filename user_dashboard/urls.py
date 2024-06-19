from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('manage_address/', views.address_management, name = 'manage_address'),
    path('myorders/', views.order_management, name = 'myorders'),
    path('confirm_cancel/<int:id>', views.confirm_cancel, name = 'confirm_cancel'),
    path('cancel/<int:id>', views.cancel_order, name = 'cancel_order'),
    path('edit_address/<int:id>/', views.edit_address, name = 'edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name = 'delete_address'),
    path('order_info/<int:order_id>/', views.order_details, name = "order_info"),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('request_return/<int:id>/',views.request_return, name = 'request_return'),
     

]