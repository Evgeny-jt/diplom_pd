from django.db import models
from django.contrib.auth.models import AbstractUser, User

USER_TYPE = (
    ('buyer', 'Покупатель'),
    ('shop', 'Магазин'),
)

ORDER_STATUS = (
    ('basket', 'В корзине'),
    ('paid', 'Оплачен'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

class User(AbstractUser):
#    pass

    def __str__(self):
        return self.username


class Shop(models.Model):
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', related_name='shop')
    name = models.CharField(max_length=100, verbose_name='Магазин')
    url = models.URLField(verbose_name='Веб-сайт', blank=True, null=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Category(models.Model):
    shop = models.ManyToManyField(Shop,  verbose_name='магазин', related_name='categories', blank=True)
    name = models.CharField(max_length=100, verbose_name='категория')

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'
#        ordering = ('-name',)
#
    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.manager.Manager()
    category = models.ForeignKey(Category, verbose_name='категория', related_name='products', blank=True, null=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='товар')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

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
        verbose_name_plural = 'Информация о продукте'

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Параметер')

    class Meta:
        verbose_name = 'Параметер'
        verbose_name_plural = 'Список параметров'

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о товаре',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товара'

    def __str__(self):
        return f'Параметр товара {self.id}'


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='buyer')
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец', related_name='salesman', blank=True, null=True)
    dt = models.DateTimeField(auto_now_add=True, verbose_name='дата заказа')
    status = models.CharField(max_length=25, verbose_name='Статус', choices=ORDER_STATUS, default='на подтверждении')

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'

    def __str__(self):
        return f'Заказ - {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='order_item', blank=True, null=True)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE,  verbose_name='Информация товара', related_name='order_item', blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин', blank=True, null=True)
    # price = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Цена', blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество', blank=True, null=True)
    # order_amount = models.PositiveIntegerField(verbose_name='Сумма', blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)

    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f'{self.user} {self.city} {self.phone}'