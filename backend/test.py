import random
import json
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact, \
    MailConfirmationCode

def save_token_file(token, name):
    if name == 'salesman1_pytest_api' or name == 'buyer1_pytest_api':
        dict_json = {'token': f'{token}'}
        with open(f'tests/backend/token_{name}.json', 'w') as f:
            json.dump(dict_json, f)
    return

def save_product_info_file(shop, name):
    if str(name) == 'salesman1_pytest_api':
        with open('tests/backend/token_salesman1_pytest_api.json', encoding='utf-8') as file:
            json_data = json.load(file)
        token = json_data['token']
        shop_id = Shop.objects.get(name=shop).id
        pi = ProductInfo.objects.filter(shop=shop)
        n = 0
        product_info_id = ''
        for data in pi:
            n += 1
            product_info_id += f'{str(data.id)}, '
            if n == 3:
                break
        dict_json = {'token': f'{token}', 'shop_id': f'{shop_id}', 'product_info_id': f'{product_info_id[0:-2]}'}
        with open(f'tests/backend/token_{name}.json', 'w') as f:
            json.dump(dict_json, f)
    return

def save_order_file(user):
    if str(user) == 'buyer1_pytest_api':
        with open('tests/backend/token_buyer1_pytest_api.json', encoding='utf-8') as file:
            json_data = json.load(file)
        token = json_data['token']
        user_id = User.objects.get(username=str(user)).id
        order_id = Order.objects.get(buyer=user_id).id
        order_item_id = OrderItem.objects.latest('id').id
        dict_json = {'token': f'{token}', 'order': order_id, 'order_item': order_item_id}

        print('-------', order_item_id)


        with open(f'tests/backend/token_{str(user)}.json', 'w') as f:
            json.dump(dict_json, f)
    return

