from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'image', 'description', 'price', 'category','rating','key_features']    
        
        
class DetailedProductSerializer(serializers.ModelSerializer):   
    similar_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'image', 'description', 'price', 'similar_products', 'category']    
    
    def get_similar_products(self, product):
        similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
        return ProductSerializer(similar_products, many=True).data
    
       
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = CardItem
        fields = ['id', 'product', 'quantity','total']
        
    def get_total(self, item):
        return item.product.price * item.quantity
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'cart_code', 'user', 'paid', 'items', 'sum_total', 'num_of_items', 'created_at', 'modified_at']

    def get_sum_total(self, cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())

    def get_num_of_items(self, cart):
        return sum(item.quantity for item in cart.items.all())


class SimpleCartSerializers(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'cart_code', 'num_of_items']

    def get_num_of_items(self, cart):
        return sum(item.quantity for item in cart.items.all())



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):   
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id","username","first_name","last_name","email","city","state","address","phone"]
        
