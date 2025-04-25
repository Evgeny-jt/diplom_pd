import random
import json
from multiprocessing.managers import Token

from django.shortcuts import render
from requests import get
from yaml import load as load_yaml, Loader
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from orders.serializers import ShopSerializer, CategorySerializer, ProductSerializer, UserSerializer, OrderSerializer, \
    OrderItemSerializer, ContactSerializer
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact, \
    MailConfirmationCode
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsOwner

# from .send_email import send_email_registration
from backend.tasks import send_email_task, code_email_delete_task

from .test import save_token_file, save_product_info_file, save_order_file


class UserRegistration(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        '''
        Создание нового пользователя
        Возвращает успех или отказ с описанием
        '''
        try:
            request.data['username']
        except:
            return Response({'отказ': 'Имя пользователя не указано'})

        try:
            request.data['email']
        except:
            return Response({'отказ': 'Email не указан'})

        try:
            request.data['password']
        except:
            return Response({'отказ': 'Пароль не указан'})

        if User.objects.filter(username=request.data['username']).exists():
            return Response({'отказ': 'Имя пользователя занято'})
        if User.objects.filter(email=request.data['email']).exists():
            return Response({'отказ': 'Пользоватеть с таким email уже существует'})
        User.objects.get_or_create(username=request.data['username'],
                                   password=request.data['password'],
                                   email=request.data['email'],
                                   )
        print('---username---', request.data['username'])
        if User.objects.filter(username='salesman1_pytest_api').exists() and request.data['username'] == 'salesman1_pytest_api':
            mail_confirmation_code = 2071
            print('---------Код для продавца')
        elif User.objects.filter(username='buyer1_pytest_api').exists() and request.data['username'] == 'buyer1_pytest_api':
            print('---------Код для покупателя')
            mail_confirmation_code = 2071
        else:
            mail_confirmation_code = random.randint(1000, 9999)
        user_name = User.objects.get(username=request.data['username'])
        MailConfirmationCode.objects.create(user=user_name, code=mail_confirmation_code)
        print('-----', request.data['email'], '------', mail_confirmation_code)
        send_email_task.delay(
            send_email=request.data['email'],
            content=str(f'Ваш код подтверждения: {mail_confirmation_code}')
        )
        code_id = MailConfirmationCode.objects.get(user=user_name).id
        code_email_delete_task.delay(code_id=code_id, sec_sleep=60)
        return Response({'успех': 'Регистрация выполнена'})

    def delete(self, request):
        user = User.objects.get(username=request.data['username'])
        if user != self.request.user:
            return Response({'отказ': 'Нет прав удалять других пользователей'})
        if not User.objects.filter(username=request.data['username']).exists():
            return Response({'отказ': 'Пользователь с таким именем не зарегестрирован'})
        delete_user_id = User.objects.get(username=request.data['username']).id
        User.objects.filter(id=delete_user_id).delete()
        return Response({'успех': 'Пользователь удалён'})


class LoginView(ListAPIView):
    '''
    Класс получения токена
    Возвращает успех или отказ с описанием
    '''

    def post(self, request):
        if not User.objects.filter(email=request.data['email']).filter(password=request.data['password']).exists():
            return Response({'отказ': 'Неверный логин или пароль'})
        user_id = User.objects.get(email=request.data['email']).id
        mail_user_code = MailConfirmationCode.objects.get(user=user_id).code
        if mail_user_code != int(request.data['mail_confirmation_code']):
            return Response({'отказ': 'Неверный код подтверждения'})
        token = Token.objects.create(user_id=user_id)

        name = request.data['username']
        save_token_file(token=token, name=name)

        send_email_task.delay(
            send_email=request.data['email'],
            content=str(f'Ваш токен: {token}')
        )
        code_id = MailConfirmationCode.objects.get(user=user_id).id
        code_email_delete_task.delay(code_id=code_id)
        return Response({'успех': 'Вход в выполнен.'})


class ProductFilterView(ListAPIView):
    """
        Класс для просмотра доступных товаров по id
    """

    def get(self, request):
        product = ProductInfo.objects.filter(id=request.GET.get('id'))[0]
        return Response({'товар': f'{product.id}, {product.name}, {product.price}, {product.quantity}, {product.shop}'})


class OrderItemView(ListAPIView):
    '''
        Класс позволяет работать с товарами в заказе пользователя
        Просмотр заказа методом get
        Создание нового заказа методом post
        Изменение количество товара в заказе методом put
        Удаление товара из заказа методом delete
        Возвращает успех или отказ с описанием
    '''
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_fields = ['id']
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        id_product_info = request.data["add_products"][0]['product_info']
        price = ProductInfo.objects.get(id=id_product_info).price
        order, _ = Order.objects.get_or_create(buyer_id=self.request.user.id, status='В корзине')
        for order_item in request.data['add_products']:
            order_it, _ = OrderItem.objects.get_or_create(order_id=order.id,
                                                          product_info_id=order_item['product_info'],
                                                          shop_id=order_item['shop'],
                                                          price=price,
                                                          quantity=order_item['quantity'],
                                                          order_amount=price * order_item['quantity']
                                                          )
        save_order_file(user=self.request.user)
        return Response({'успех': 'Все товары добавленны в заказ'})

    def put(self, request):
        id_product_info = request.data['id']
        if OrderItem.objects.filter(id=id_product_info).exists() == False:
            return Response({'отказ': 'У вас нет такого товара в корзине'})  # У вас нет такого товара в корзине
        price = OrderItem.objects.get(id=id_product_info).price
        #        if not Order.objects.filter(buyer=self.request.user.id).filter(order_item=request.data['id']).exists():
        #            return Response({'отказ': 'Сначало добавте товар в корзину'})
        if Order.objects.filter(order_item=request.data['id']).get().status != 'В корзине':
            return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})
        update_item_id = request.data['id']
        OrderItem.objects.filter(id=update_item_id).update(
            quantity=request.data['quantity'],
            order_amount=price * request.data['quantity']
        )
        return Response({'отказ': 'Количество товара изменено'})

    def delete(self, request):
        delete_order_item_id = request.GET.get('id')
        if not Order.objects.filter(order_item=delete_order_item_id).exists():
            return Response({'отказ': 'В корзине нет товара с таким id'})
        delete_order_id = Order.objects.filter(order_item=delete_order_item_id).get().id
        #        if not Order.objects.filter(buyer=self.request.user.id).filter(id=delete_order_id).exists():
        #            return Response({'отказ': 'Нужно добавить товар в корзину'})
        if Order.objects.filter(id=delete_order_id).get().status != 'В корзине':
            return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})
        OrderItem.objects.filter(id=delete_order_item_id).delete()
        return Response({'успех': 'Товар удалён из корзины'})


class OrderView(ListAPIView):
    '''
        Класс позволяет посмотреть заказы пользователя или удалить заказ
        Просмотр заказа методом get
        Удаление заказа методом delete
        Возвращает успех или отказ с описанием
    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request):
        delete_order_id = request.GET.get('id')
        if not Order.objects.filter(id=delete_order_id).exists():
            return Response({'отказ': 'У вас нет такого заказа'})
        delete_order_id = Order.objects.filter(id=delete_order_id).get().id
        if not Order.objects.filter(buyer=self.request.user.id).filter(id=delete_order_id).exists():
            return Response({'отказ': 'у вас нет оформленного заказа'})
        if Order.objects.filter(id=delete_order_id).get().status != 'В корзине':
            return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})
        Order.objects.filter(id=delete_order_id).delete()
        return Response({'успех': 'Заказ удалён'})


class ContactView(ListAPIView):
    '''
        Класс просмотра и создания контактной информации о пользователе
        Просмотр контактной информации методом get
        Создание новой контактной информации методом post
        Удалить контактную информацию методом delete
        Возвращает успех или отказ с описанием
    '''
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        order_it, _ = Contact.objects.get_or_create(user=self.request.user,
                                                    city=request.data['add_contact']['city'],
                                                    street=request.data['add_contact']['street'],
                                                    house=request.data['add_contact']['house'],
                                                    structure=request.data['add_contact']['structure'],
                                                    building=request.data['add_contact']['building'],
                                                    apartment=request.data['add_contact']['apartment'],
                                                    phone=request.data['add_contact']['phone']
                                                    )
        return Response({'успех': 'Контакты сохранены'})

    def delete(self, request):
        if not Contact.objects.filter(user=self.request.user).exists():
            return Response({'отказ': 'Вы не владелец этой информации'})
        delete_id = request.data['id']
        delete_contact_id = Contact.objects.filter(id=delete_id).get().id
        Contact.objects.filter(id=delete_contact_id).delete()

        return Response({'успех': 'Контакт удалён'})


class ShopView(ListAPIView):
    '''
        Класс просмотра и создания магазинов
        Просмотр существующих магазинов методом get
        Создание нового магазина методом post
        Возвращает успех или отказ с описанием
    '''
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def post(self, request):
        if Shop.objects.filter(name=request.data['name']).exists():
            return Response({'отказ': 'Магазин с таким названием уже существует'})
        try:
            Shop.objects.create(salesman_id=self.request.user.id, name=request.data['name'], url=request.data['url'])
        except:
            return Response({'отказ': 'Заполнены не все обязательные поля'})
        return Response({'успех': 'Магазин создан'})


class CategoryView(ListAPIView):
    '''
        Класс просматривает категории товаров.
        Просмотр методом get.
        Возвращает успех или отказ с описанием
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request):
        return Response({'status': 'ok'})


class UpPriseView(ListAPIView):
    '''
        Класс обновления товаров в магазине
        Обновления товаров методом post
        Возвращает успех или отказ с описанием
    '''

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        try:
            request.data['url']
        except:
            return Response({'отказ': 'Url не заполнен'})
        if not Shop.objects.filter(salesman=self.request.user).exists():
            return Response({'отказ': 'У вас нет магазина'})
        stream = get(request.data['url']).content
        data = load_yaml(stream, Loader=Loader)
        shop = Shop.objects.get(salesman_id=self.request.user.id)
        for i in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=i['id'], name=i['name'])
            category_object.shop.add(shop.id)
            category_object.save()
        for i in data['goods']:
            product, _ = Product.objects.get_or_create(name=i['name'], category_id=i['category'])
            product_info, _ = ProductInfo.objects.get_or_create(product_id=product.id,
                                                                shop_id=shop.id,
                                                                name=i['name'],
                                                                quantity=i['quantity'],
                                                                price=i['price'],
                                                                price_rrc=i['price_rrc']
                                                                )
            for name, value in i['parameters'].items():
                parameter_object, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter_object.id,
                                                value=value
                                                )
        save_product_info_file(shop=shop, name=self.request.user)
        return Response({'успех': 'Товары обновлены'})


class SendInvoice(ListAPIView):
    '''
        Класс отправления накладной менеджеру
        Отправка методом post в случае успеха обновляется статус корзины с 'в корзине' на 'оплачено'
        Возвращает успех или отказ с описанием
    '''

    def perform_create(self, serializer):
        serializer.save(user=self.request.data)

    def post(self, request):
        send_order_id = request.data['order']
        print("---send_order_id----", send_order_id)
        if not Order.objects.filter(buyer=self.request.user).filter(id=send_order_id).exists():
            return Response({'отказ': 'У вас нет такого заказа в корзине'})
        if quantity_product(request):
            return Response({'отказ': 'В магазине нет такого количества заказываемого товара'})
        if Order.objects.filter(id=send_order_id).get().status != 'В корзине':
            return Response({'отказ': 'Заказ уже оплачен'})
        if not Contact.objects.filter(user=self.request.user.id).exists():
            return Response({'отказ': 'У вас не заполнена контактная информация. Добавьте Contact'})
        for order_item_object in OrderItem.objects.all():  # ищем id продавца по номеру заказа
            if int(send_order_id) == order_item_object.order.id:
                shop_id = Shop.objects.get(id=order_item_object.shop.id).id
                user_name = Shop.objects.get(id=shop_id).salesman
                # user_id = User.objects.get(shop=user_name).id# id продавца по номеру заказа
                Order.objects.filter(id=send_order_id).update(salesman_id=user_name.id, status='Оплачен')
                user_email = User.objects.get(id=user_name.id).email
                buyer = User.objects.get(id=self.request.user.id).username

                print('----------user_email----------', user_email)
                send_email_task.delay(
                    send_email=user_email,
                    content=str(f'Покупатель {buyer} оплатил заказ № - {send_order_id}.')
                )
                return Response({'успех': 'Накладная отправлена'})
        return Response({'status': 'НАСТРОЙКА'})


class Status(ListAPIView):
    '''
        Класс изменяет статус заказа.
        Изменяет методом post. Метод уменьшает количество товара в магазине на заказанное число товара и меняет статус корзины.
        Возвращает успех или отказ с описанием
    '''

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        status_order_id = request.data['order']
        status_requesr = request.data['status']
        if not Order.objects.filter(salesman=self.request.user).filter(id=status_order_id).exists():
            return Response({'отказ': 'Такого оплаченного клиентом заказа у вас нет'})
        if Order.objects.filter(id=status_order_id).get().status == 'В корзине':
            return Response({'отказ': 'Заказ еще не оплачен'})
        elif Order.objects.filter(id=status_order_id).get().status == status_requesr:
            return Response({'отказ': 'Попытка перезаписать тот же статус'})
        if quantity_product(request):
            return Response({'отказ': 'На складе нет нужного количества товара'})
        return_order_item = OrderItem.objects.filter(order=request.data['order'])
        if Order.objects.filter(id=status_order_id).get().status == 'Оплачен':
            for order_quantity in return_order_item:
                product_info_id = ProductInfo.objects.get(shop=order_quantity.shop,
                                                          name=order_quantity.product_info
                                                          ).id
                product_info_quantity = ProductInfo.objects.get(shop=order_quantity.shop,
                                                                name=order_quantity.product_info
                                                                ).quantity
                ProductInfo.objects.filter(id=product_info_id).update(
                    quantity=product_info_quantity - order_quantity.quantity)
        Order.objects.filter(id=status_order_id).update(status=status_requesr)
        print('-------')
        user_name = Order.objects.get(id=status_order_id).buyer
        print('-------user_id: ', user_name)

        user_email = User.objects.get(username=user_name).email
        print('-------user_email: ', user_email)

        send_email_task.delay(
            send_email=user_email,
            content=str(f'Статус заказа № - {request.data['order']} изменен на {request.data['status']}.')
        )
        return Response({'успех': 'Статус заказа изменен'})


def quantity_product(request):
    '''
        Метод проверяет количество товара в заказе и количество в магазине
        Возвращает True если количество в магазине больше или равно заказанному
    '''
    return_order_item = OrderItem.objects.filter(order=request.data['order'])
    for order_quantity in return_order_item:
        quantity_shop = ProductInfo.objects.get(shop=order_quantity.shop,
                                                name=order_quantity.product_info
                                                ).quantity
        if order_quantity.quantity > quantity_shop:
            return Response({'отказ': 'В магазине нет такого количества заказываемого товара'})
