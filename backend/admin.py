from django.contrib import admin
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact, MailConfirmationCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
    list_filter = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

@admin.register(MailConfirmationCode)
class MailConfirmationCode(admin.ModelAdmin):
    list_display = ['id', 'user', 'code']
    list_filter = ['id', 'user', 'code']

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'salesman']
    list_filter = ['id', 'name', 'salesman']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['id', 'name', 'category']


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
    list_display = ['id', 'buyer', 'dt', 'status']
    list_filter = ['id', 'buyer', 'dt', 'status']
    exclude = ['salesman']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_info', 'shop', 'price', 'quantity', 'order_amount']
    list_filter = ['id', 'order', 'product_info', 'shop', 'price', 'quantity', 'order_amount']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
    list_filter = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
