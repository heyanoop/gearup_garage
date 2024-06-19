from django.urls import path
from .import views
urlpatterns = [

    path('handlerequest/',views.handlerequest,name="handlerequest"),
    path('razorpay_success/',views.razorpay_success,name="razorpay_success"),
    path('retry_payment/<int:id>/',views.retry_payment, name = 'retry_payment'),
    path('handlerequest_retry/',views.handlerequest_retry,name="handlerequest_retry"),
    path('razorpay_success__retry/',views.razorpay_success__retry,name="razorpay_success__retry"),
    
   

]