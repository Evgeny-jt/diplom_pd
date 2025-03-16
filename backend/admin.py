from django.contrib import admin

from .models import Shop, Category, Product, ProductInfo, Parametr,ProductParametr, Order, OrderItem, Contact

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']
    list_filter = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['shop', 'name']
    list_filter = ['shop', 'name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name']
    list_filter = ['category', 'name']

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['product', 'shop', 'name', 'quantity', 'price', 'price_rrc']
    list_filter = ['product', 'shop', 'name', 'quantity', 'price', 'price_rrc']

@admin.register(Parametr)
class ParametrAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(ProductParametr)
class ProductParametrAdmin(admin.ModelAdmin):
    list_display = ['product_info', 'parametr', 'value']
    list_filter = ['product_info', 'parametr', 'value']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'dt', 'status']
    list_filter = ['user', 'dt', 'status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'shop', 'quantity']
    list_filter = ['order', 'product', 'shop', 'quantity']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['type', 'user', 'value']
    list_filter = ['type', 'user', 'value']
