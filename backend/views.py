from multiprocessing.managers import Token

from requests import get
from yaml import load as load_yaml, Loader

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest_passwordreset.tokens import get_token_generator

from orders.serializers import ShopSerializer, CategorySerializer, ProductSerializer, ProductInfo, UserSerializer# LoginSerializer
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter #Login
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User

class UserRegistration(ListAPIView): # регистрация пользователя
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post (self, request):
        User.objects.get_or_create(username=request.data['username'],
                                   password=request.data['password'],
                                   first_name=request.data['first_name'],
                                   last_name=request.data['last_name'],
                                   email=request.data['email'],
                                   )
        # # user = request.data['username'].save()
        # user.set_password(request.data['password'])
        # user.save()
        return Response({'status UserRegistration': 'ok'})


class LoginView(ListAPIView):
#     queryset = Login.objects.all()
#     serializer_class = LoginSerializer

    def post(self, request):
        print('email: ', request.data['email'], 'пароль: ', request.data['password'])
        # t =get_token_generator().generate_token()
        name = User.objects.all().filter(email='dylan_jt@mail.ru')
        user = User.objects.get(username=name[0].username)
        token = Token.objects.create(user=user)

        print('---token: ', token)


        return Response({'Вход в выполнен.': f' TOKEN: {token}'})




class ShopView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def post(self, request):
        Shop.objects.create(name=request.data['name'], url=request.data['url'])
        return Response({'status': 'ok'})

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

    def post(self, request):
        # wu = Shop.objects.get(id=6)
        wu = Shop.objects.all().filter(id=1) # id магазина который хотим рбновить

        print('---', wu[0].url)

        stream = get(wu[0].url).content

        data = load_yaml(stream, Loader=Loader)
# давить проверку если магазин существует не создавать его
        print('---', data['shop'])
        # Shop.objects.create(name=data['shop'], url=['www.test.ru'])
        Shop.objects.get_or_create(name=data['shop'], url=['www.test.ru'])

        # print('---id shop')
        queryset = Shop.objects.all().filter(name=data['shop'])
        # print('---id shop', queryset[0].id)
        #
        # print('---', data['categories'])
        shop, _ = Shop.objects.get_or_create(name=data['shop'])#, user_id=request.user.id)
        for i in data['categories']:
            print('-categoru i-', i)
            # print('-qyeryset-', queryset[0].id)
            category_object, _ = Category.objects.get_or_create(id=i['id'],name=i['name'])
            category_object.shop.add(shop.id)
            category_object.save()

        for i in data['goods']:
            product, _ = Product.objects.get_or_create(name=i['name'],  category_id=i['category'])

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




            # Product.objects.get_or_create(name=i['name'], category_id=i['category'])


            # category_object, _ = Category.objects.get_or_create(name=i['name'])
            # category_object.shop.add(queryset[0].id)
            # category_object.save()



        # n = 1
        # for i in data:
        #     print('-', n, '---', i)
        #     n += 1
        #
        #     - 1 - -- shop
        #     - 2 - --
        #     - 3 - --

        # Shop.objects.create(name=request.data['name'], url=request.data['url'])
        return Response({'status': 'ok'})
