from django.contrib import admin

from .models import Shop, Category, Product, ProductInfo, Parameter,ProductParameter, Order, OrderItem, Contact

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
    list_display = ['id', 'product', 'shop', 'name', 'quantity', 'price', 'price_rrc']
    list_filter = ['id', 'product', 'shop', 'name', 'quantity', 'price', 'price_rrc']

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
    list_display = ['id', 'order', 'product', 'shop', 'quantity']
    list_filter = ['id', 'order', 'product', 'shop', 'quantity']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'user', 'value']
    list_filter = ['id', 'type', 'user', 'value']
