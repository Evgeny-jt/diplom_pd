from multiprocessing.managers import Token
from unicodedata import category

from django.http import JsonResponse
from requests import get
from yaml import load as load_yaml, Loader

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest_passwordreset.tokens import get_token_generator


from orders.serializers import ShopSerializer, CategorySerializer, ProductSerializer, ProductInfo, UserSerializer, OrderSerializer, OrderItemSerializer, ContactSerializer
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from backend.permissions import IsOwner


class UserRegistration(ListAPIView): # регистрация пользователя
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post (self, request):
        User.objects.get_or_create(username=request.data['username'],
                                   password=request.data['password'],
                                   # first_name=request.data['first_name'],
                                   # last_name=request.data['last_name'],
                                   email=request.data['email'],
                                   )
        return Response({'status UserRegistration': 'ok'})


class LoginView(ListAPIView):
#     queryset = Login.objects.all()
#     serializer_class = LoginSerializer

    def post(self, request):
        # t =get_token_generator().generate_token()
        name = User.objects.all().filter(email='dylan_jt@mail.ru')
        user = User.objects.get(username=name[0].username)
        token = Token.objects.create(user=user)
        return Response({'Вход в выполнен.': f' TOKEN: {token}'})


class ProductFilterView(ListAPIView):
    """
    Класс для просмотра категорий
    """
    def get(self, request):
        a = ProductInfo.objects.all().select_related('product').filter(name='Samsung QLED Q90R 65" 4K UHD Smart TV')
        for i in a:
            print(i.id,  i.product.category,   i.product.name,    i.shop,   i.price,   i.quantity)

        return Response({'ok': f'{a}'})


class OrderItemView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_fields = ['id']
    # permission_classes = [IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get(self, request):
    #     return Response({'status': 'ok'})

    def post(self, request):
        shop_id = Shop.objects.get(id=request.data['add_products'][0]['shop'])
        id_product_info = request.data["add_products"][0]['product_info']
        print('---', id_product_info)
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
        return Response({'status': 'ok'})
    
    def put(self, request):
        id_product_info = request.data['id']
        price = OrderItem.objects.get(id=id_product_info).price
        try:
            Order.objects.filter(order_item=request.data['id']).get().id
        except:
            return Response({'У вас нет такого товара в корзине'})
        else:
            try:
                Order.objects.filter(buyer=self.request.user.id).filter(order_item=request.data['id']).get()
            except:
                return Response({'отказ': 'Сначало добавте товар в корзину'})
            else:
                if Order.objects.filter(order_item=request.data['id']).get().status != 'В корзине':
                    return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})

                update_item_id = request.data['id']
                OrderItem.objects.filter(id=update_item_id).update(
                                                                   quantity=request.data['quantity'],
                                                                   order_amount=price * request.data['quantity']
                )
                return Response({'status': 'Количество товара изменено'})


    def delete(self, request):
        delete_order_item_id = request.GET.get('id')
        try:
            delete_order_id = Order.objects.filter(order_item=delete_order_item_id).get().id
        except:
            return Response({'отказ': 'У вас нет такого товара в корзине'})
        else:
            try:
                Order.objects.filter(buyer=self.request.user.id).filter(id=delete_order_id).get()
            except:
                return Response({'отказ': 'Сначало добавте товар в корзину'})
            else:
                if Order.objects.filter(id=delete_order_id).get().status != 'В корзине':
                    return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})
                OrderItem.objects.filter(id=delete_order_item_id).delete()
                return Response({'status': 'Товар удалён из корзины'})


class OrderView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request):
        delete_order_id = request.GET.get('id')
        print(delete_order_id)
        try:
            delete_order_id = Order.objects.filter(id=delete_order_id).get().id
            print(delete_order_id)
        except:
            return Response({'отказ': 'У вас нет такого заказа'})
        else:
            try:
                Order.objects.filter(buyer=self.request.user.id).filter(id=delete_order_id).get()
            except:
                return Response({'отказ': 'у вас нет оформленного заказа'})
            else:
                if Order.objects.filter(id=delete_order_id).get().status != 'В корзине':
                    return Response({'отказ': 'Заказ уже оплачен и перемещен из корзины'})
                Order.objects.filter(id=delete_order_id).delete()
                return Response({'status': 'заказ удалён'})
        return Response({'status': 'НАСТРОЙКА'})


class ContactView(ListAPIView):
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
        return Response({'status': 'Контакты сохранены'})


class ShopView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def post(self, request):
        Shop.objects.create(salesman_id=self.request.user.id, name=request.data['name'], url=request.data['url'])
        return Response({'status': 'Магазин создан'})

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request):
        return Response({'status': 'ok'})

class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request):
        return Response({'status': 'ok'})

class UpPriseView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        try:
            Shop.objects.get(salesman_id=self.request.user.id)
        except:
            return Response({'отказ': 'У вас нет магазина'})
        else:
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
                                                    value=value)
            return Response({'status': 'Товары обнавлены'})


class SendInvoice(ListAPIView):

    def perform_create(self, serializer):
        serializer.save(user=self.request.data)

    def post(self, request):
        send_order_id = request.data['order']
        try:
            Order.objects.filter(buyer=self.request.user).filter(id=send_order_id).get().id
        except:
            return Response({'отказ': 'У вас нет токого заказа в корзине'})
        else:
            if quantity_product(request):
                return Response({'отказ': 'В магазине нет такого количества заказываемого товара'})
            if Order.objects.filter(id=send_order_id).get().status != 'В корзине':
                return Response({'отказ': 'Заказ уже оплачен'})
            try:
                Contact.objects.get(user=self.request.user.id)
            except:
                return Response({'отказ': 'У вас не заполнена контактная информация. Добавьте Contact'})
            else:
                for order_item_object in OrderItem.objects.all(): # ищем id продовца по номеру заказа
                    if int(send_order_id) == order_item_object.order.id:
                        shop_id = Shop.objects.get(id=order_item_object.shop.id).id
                        print('-shop-', shop_id)
                        user_name = Shop.objects.get(id=shop_id).salesman
                        print('-user_name-', user_name.id)
                        # user_id = User.objects.get(shop=user_name).id# id продовца по номеру заказа
                        Order.objects.filter(id=send_order_id).update(salesman_id=user_name.id, status='Оплачен')
                        return Response({'status': 'Накладная отправлена'})
        return Response({'status': 'НАСТРОЙКА'})



class Status(ListAPIView):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        status_order_id = request.data['order']
        status_requesr = request.data['status']

        try:
            Order.objects.filter(salesman=self.request.user).filter(id=status_order_id).get()
        except:
            return Response({'отказ': 'Такого оплаченого клиентом заказа у вас нет'})
        else:
            if Order.objects.filter(id=status_order_id).get().status == 'В корзине':
                return Response({'отказ': 'Заказ еще не оплачен'})
            elif Order.objects.filter(id=status_order_id).get().status == status_requesr:
                return Response({'отказ': 'Попытка перезаписать тотже статус'})
            # изменить количество товара в магазине
            if quantity_product(request):
                return Response({'status': 'На складе нет нужного количества товара'})
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
                        quantity=product_info_quantity - order_quantity.quantity
                    )



            Order.objects.filter(id=status_order_id).update(status=status_requesr)
            return Response({'status': 'Статус заказа изменен'})
        return Response({'status': 'Настройка'})


def quantity_product(request):
    return_order_item = OrderItem.objects.filter(order=request.data['order'])
    for order_quantity in return_order_item:
        quantity_shop = ProductInfo.objects.get(shop=order_quantity.shop,
                                                name=order_quantity.product_info
                                                ).quantity
        if order_quantity.quantity > quantity_shop:
            return Response({'отказ': 'В магазине нет такого количества заказываемого товара'})