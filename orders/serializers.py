from rest_framework import serializers

from backend.models import Shop, Category, Product, ProductInfo, ProductParametr, Order, OrderItem, Contact


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'shop', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name']

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'name', 'quantity', 'price', 'price_rrc']

class ParametrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['id', 'name']

class ProductParametrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParametr
        fields = ['id', 'product_info', 'parametr', 'value']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'dt', 'status']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'shop', 'quantity']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type', 'user', 'shop', 'value']
