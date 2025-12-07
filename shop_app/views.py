from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data)    

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailedProductSerializer
    lookup_field = 'id'
    

class AddCartItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        if not cart_code or not product_id:
            return Response({"error": "cart_code and product_id required"}, status=400)

        try:
            cart, _ = Card.objects.get_or_create(cart_code=cart_code)
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID"}, status=404)

        item, _ = CardItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = 1
        item.save()

        serializer = self.get_serializer(item)
        return Response({"data": serializer.data, "message": "Cart item added"}, status=201)
    
class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart_code = self.request.query_params.get('cart_code')
        return CardItem.objects.filter(cart__cart_code=cart_code)
    
class SimpleCartView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = SimpleCartSerializers
    lookup_field = 'cart_code'

class CartView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'cart_code' 
    
class UpdateCartItemQuantityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CardItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'id' 

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class UserInfo(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # return the logged-in user
        return self.request.user
    
