from django.urls import path
from .views import RazorpayOrderAPIView, TransactionAPIView

urlpatterns = [
    path("order/create/",RazorpayOrderAPIView.as_view(), name="razorpay-create-order-api"),
    path("order/complete/",TransactionAPIView.as_view(), name="razorpay-complete-order-api"),
]