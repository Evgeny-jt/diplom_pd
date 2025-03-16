from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import ShopSerializer, CategorySerializer
from .models import Shop, Category


# @api_view(['GET'])
# def test(request):
#     print('запрос в базу')
#     shop = Shop.objects.all()
#     ser = ShopSerializer(shop, many=True)
#     print('shop - ', shop)
#     data = {'jt': 'jt_test1'}
#     return Response(ser.data)


# class OrderView(APIView):
#     def get(self, request):
#         shop = Shop.objects.all()
#         ser = ShopSerializer(shop, many=True)
#         return Response(ser.data)
#
#     def post(self, request):
#         return Response({'status': 'ok'})

class OrderView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def post(self, request):
        return Response({'status': 'ok'})

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request):
        return Response({'status': 'ok'})