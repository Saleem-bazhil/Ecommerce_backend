from django.urls import path
from .views import *

urlpatterns = [
    path('products/', products, name='products'),
    path('productsDetails/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('addCartItem/', AddCartItemView.as_view(), name='add_cart_item'),
    path('cartItems/', CartItemListView.as_view(), name='cart_item_list'),
    path('simpleCart/<str:cart_code>/', SimpleCartView.as_view(), name='simple_cart'),
    path('cart/<str:cart_code>/', CartView.as_view(), name='cart-detail'),
    path('updateCartItem/<int:id>/', UpdateCartItemQuantityView.as_view(), name='update_cart_item_quantity'),
    path('userInfo/',UserInfo.as_view(),name="user_info"),
]
