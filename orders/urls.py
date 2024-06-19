from django.urls import path
from .import views
urlpatterns = [

    path('place_order/',views.place_order,name="place_order"),
     path('order/invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    
    
   

]