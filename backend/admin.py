from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
    list_filter = ['id', 'username', 'password', 'email', 'first_name', 'last_name']



@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']
    list_filter = ['id', 'name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ['id', 'shop', 'name']
    # list_filter = ['id', 'shop', 'name']
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name']
    list_filter = ['id', 'category', 'name']

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'shop', 'price','quantity']
    list_filter = ['id', 'name', 'shop', 'price','quantity']

@admin.register(Parameter)
class ParametrAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']

@admin.register(ProductParameter)
class ProductParametrAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_info', 'parameter', 'value']
    list_filter = ['id', 'product_info', 'parameter', 'value']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dt', 'status']
    list_filter = ['id', 'user', 'dt', 'status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_info', 'shop', 'quantity']
    list_filter = ['id', 'order', 'product_info', 'shop', 'quantity']




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
    list_filter = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
