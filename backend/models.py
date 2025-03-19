from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = (
    ('buyer', 'Покупатель'),
    ('shop', 'Магазин'),
)

class User(AbstractUser):
    type = models.CharField(max_length=30, verbose_name='Тип пользователя', choices=USER_TYPE, null=False, blank=False)
    surname = models.CharField(max_length=60, verbose_name='Отчество', blank=True)
    company = models.CharField(max_length=60, verbose_name='Компания', blank=True)
    position = models.CharField(max_length=100, verbose_name='Должность', blank=True)

    class Meta:
        verbose_name = 'Имя'
        verbose_name_plural = 'Имя'

    def __str__(self):
        return self.username


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='Магазин')
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Магазин1'
        verbose_name_plural = 'Магазины2'

    def __str__(self):
        return self.name


class Category(models.Model):
    shop = models.ManyToManyField(Shop, related_name='categories', blank=True)
    name = models.CharField(max_length=100, verbose_name='Категория')
    # external_id = models.PositiveIntegerField(verbose_name='Внешний ИД', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.manager.Manager()
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True, null=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Продукт')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товарыы'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Информация')
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    price_rrc = models.IntegerField()

    class Meta:
        verbose_name = 'Добавить информацию'
        verbose_name_plural = 'Информация продукта'

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Параметер')

    class Meta:
        verbose_name = 'Параметер'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Параметры подукта'
        verbose_name_plural = 'Параметр продукта'

    # def __str__(self):
    #     return self.name


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
