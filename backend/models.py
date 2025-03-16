from django.db import models
from django.contrib.auth.models import User



# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=25)
#     email = models.EmailField(unique=True)


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Магазин')
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Продукт')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Информация')
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    price_rrc = models.IntegerField()

    class Meta:
        verbose_name = 'Добавить информацию'
        verbose_name_plural = 'Информация продукта'

    def __str__(self):
        return self.name


class Parametr(models.Model):
    name = models.CharField(max_length=100, verbose_name='Параметр')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.name


class ProductParametr(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parametr = models.ForeignKey(Parametr, on_delete=models.CASCADE, verbose_name='Параметр продукта')
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Параметры подукта'
        verbose_name_plural = 'Параметр'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ордер')
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордер'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Пункт заказа')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Пункт заказа'
        verbose_name_plural = 'Пункт заказа'

    def __str__(self):
        return self.name


class Contact(models.Model):
    type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Контакт')
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name
