import pytest
import requests


@pytest.fixture
def salesman_registration_json():
    json = {
        "username": "salesman1_pytest_api",
        "password": "s1e341e3f8a2c92b98d6a90f66384621ffe6",
        "email": "dylan_jt@mail.ru",
        "mail_confirmation_code": "2071"
    }
    return json


@pytest.fixture
def buyer_registration_json():
    json = {
        "username": "buyer1_pytest_api",
        "password": "b1e441e4f8j2c92b78d6a90f66u84621ffe6",
        "email": "enny2010@yandex.ru",
        "mail_confirmation_code": "2071"
    }
    return json


@pytest.fixture
def salesman1():
    return 'tests/backend/token_salesman1_pytest_api.txt'

@pytest.fixture
def buyer1():
    return 'tests/backend/token_buyer1_pytest_api.txt'


### Удалить пользователя (продавец)
# def test_1_salesman_delete(salesman1):
#    with open(salesman1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    json = {"username": "salesman1_pytest_api"}
#    response = requests.delete("http://127.0.0.1:8000/user/", json=json, headers=headers)
#    print(response.status_code)
#    assert response.text == '{"успех":"Пользователь удалён"}'


### Удалить пользователя (покупатель)
# def test_2_buyer_delete(buyer1):
#    with open(buyer1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    json = {"username": "buyer1_pytest_api"}
#    response = requests.delete("http://127.0.0.1:8000/user/", json=json, headers=headers)
#    print(response.status_code)
#    assert response.text == '{"успех":"Пользователь удалён"}'

### регистрация пользователя (покупатель)
# def test_4_create_user_buyer(buyer_registration_json):
#    response = requests.post("http://127.0.0.1:8000/user/register/", json=buyer_registration_json)
#    assert response.text == '{"успех":"Регистрация выполнена"}'



### регистрация пользователя (продавец)
# def test_3_create_user_salesman(salesman_registration_json):
#    response = requests.post("http://127.0.0.1:8000/user/register/", json=salesman_registration_json)
#    assert response.text == '{"успех":"Регистрация выполнена"}'


### регистрация без имени пользователя
def test_5_create_user_no_user_name():
  json = {"password": "8ae341e3f8a2c92b98d6a90f66384621ffe6", "email": "test@mail.ru"}
  response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
  assert response.text == '{"отказ":"Имя пользователя не указано"}'


### регистрация без пороля
def test_6_create_user_no_password():
  json = {"username": "test_user_0", "email": "dylan_jt@mail.ru"}
  response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
  assert response.text == '{"отказ":"Пароль не указан"}'


### регистрация пользователя без почты
def test_7_create_user_no_email():
  json = {"username": "test_user_0", "password": "8ae341e3f8a2c92b98d6a90f66384621ffe6"}
  response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
  assert response.text == '{"отказ":"Email не указан"}'


### регистрация пользователя с занятым именем
def test_8_create_user_with_taken_name(salesman_registration_json):
  response = requests.post("http://127.0.0.1:8000/user/register/", json=salesman_registration_json)
  assert response.text == '{"отказ":"Имя пользователя занято"}'


### получить список пользователей
def test_9_get_list_user():
  response = requests.get("http://127.0.0.1:8000/user/")
  assert response.status_code == 200

### вход пользователя c неверным логином или паролем
def test_10_user_login_folse():
  json = {"email": "tteesstt@mail.ru", "password": "user1"}
  response = requests.post("http://localhost:8000/user/login/", json=json)
  assert response.text == '{"отказ":"Неверный логин или пароль"}'


### вход пользователя (продавец)
# def test_11_user_salesman_login(salesman_registration_json):
#   response = requests.post("http://localhost:8000/user/login/", json=salesman_registration_json)
#   assert response.text == '{"успех":"Вход в выполнен."}'


### вход пользователя (покупатель)
# def test_11_user_buyer_login(buyer_registration_json):
#   response = requests.post("http://localhost:8000/user/login/", json=buyer_registration_json)
#   assert response.text == '{"успех":"Вход в выполнен."}'


### создать магазин с неверным токеном
def test_13_create_shop_invalid_token():
   #Arrange
   invalid_token={'Authorization': 'Token ee5550f707475e92a1c151e6a75eb61a6ecabd'}
   json = {"name": " Связной_test", "url": "www.связной.ру"}
   response = requests.post("http://localhost:8000/shop/", json=json, headers=invalid_token)
   assert response.text == '{"detail":"Invalid token."}'


### создать магазин с верным токеном
# def test_14_create_shop_correct_token(salesman1):
#    with open(salesman1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    json = {"name": " Связной_test", "url": "www.связной.ру"}
#    response = requests.post("http://localhost:8000/shop/", json=json, headers=headers)
#    assert response.text == '{"успех":"Магазин создан"}'


### Магазин с таким названием уже существует
# def test_15_create_shop_with_a_taken_name(salesman1):
   # with open(salesman1, 'r', encoding='utf-8') as file:
   #     token  = file.read()
   # headers={'Authorization': f'Token {token}'}
   # json = {"name": " Связной_test", "url": "www.связной.ру"}
   # response = requests.post("http://localhost:8000/shop/", json=json, headers=headers)
   # assert response.text == '{"отказ":"Магазин с таким названием уже существует"}'


### Заполнены не все обязательные поля при создании магазина
def test_16_create_shop_with_not_all_fields_filled_in(salesman1):
   with open(salesman1, 'r', encoding='utf-8') as file:
       token  = file.read()
   headers={'Authorization': f'Token {token}'}
   json = {"name": " Связной_test17"}
   response = requests.post("http://localhost:8000/shop/", json=json, headers=headers)
   assert response.text == '{"отказ":"Заполнены не все обязательные поля"}'


### Получить список магазинов
def test_17_get_list_shop():
  response = requests.get("http://127.0.0.1:8000/shop/")
  assert response.status_code == 200


### обновление товаров в магазине
# def test_18_up_list_shop(salesman1):
#    with open(salesman1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    json = {"url": "https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml"}
#    response = requests.post("http://localhost:8000/up/", json=json, headers=headers)
#    assert response.text == '{"успех":"Товары обновлены"}'


### обновление товаров в магазине c неверным токеном
def test_19_up_invalid_token(salesman1):
   with open(salesman1, 'r', encoding='utf-8') as file: #удалить
       token  = file.read() #удалить
   headers={'Authorization': 'Token ee5550f707475e92a1c151e6a75eb61a6ecabd'}
   json = {"url": "https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml"}
   response = requests.post("http://localhost:8000/up/", json=json, headers=headers)
   assert response.text == '{"detail":"Invalid token."}'


### Обновление товаров в магазине заполнены не все обязательные поля
def test_20_create_shop_with_not_all_fields_filled_in(salesman1):
   with open(salesman1, 'r', encoding='utf-8') as file:
       token  = file.read()
   headers={'Authorization': f'Token {token}'}
   json = {}
   response = requests.post("http://localhost:8000/up/", json=json, headers=headers)
   assert response.text == '{"отказ":"Url не заполнен"}'


### КОРЗИНА - добавить товары в корзину
def test_21_create_orderitem(buyer1):
   with open(buyer1, 'r', encoding='utf-8') as file:
       token  = file.read()
   headers={'Authorization': f'Token {token}'}
   json = {"add_products":
       [
           {
               "product_info": 144,
               "shop": 13,
               "quantity": 10
           },
           {
               "product_info": 150,
               "shop": 13,
               "quantity": 10
           }
       ]
   }
   response = requests.post("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
   assert response.text == '{"успех":"Все товары добавленны в заказ"}'



### КОРЗИНА - добавить товары в корзину c неверным токеном
def test_22_create_orderitem_invalid_token():
    invalid_token={'Authorization': 'Token ee5550f707475e92a1c151e6a75eb61a6ecabd'}
    json = {"add_products":
        [
            {
                "product_info": 10,
                "shop": 11,
                "quantity": 10
            }
        ]
    }
    response = requests.post("http://127.0.0.1:8000/orderitem/", json=json, headers=invalid_token)
    assert response.text == '{"detail":"Invalid token."}'

### КОРЗИНА - посмотреть содержание корзины
def test_23_get_list_basket(buyer1):
    with open(buyer1, 'r', encoding='utf-8') as file:
        token  = file.read()
    headers={'Authorization': f'Token {token}'}
    response = requests.get("http://127.0.0.1:8000/orderitem/", headers=headers)
    assert response.status_code == 200


### КОРЗИНА - изменить количество товара в корзине по его id
def test_24_put_quantity_by_id(buyer1):
    with open(buyer1, 'r', encoding='utf-8') as file:
        token  = file.read()
    headers={'Authorization': f'Token {token}'}
    json = {
        "id": 5,
        "quantity": 7
    }
    response = requests.put("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
    assert response.text == '{"отказ":"Количество товара изменено"}'


### КОРЗИНА - изменить количество товара по его id (неверный id)
def test_25_put_quantity_no_id(buyer1):
    with open(buyer1, 'r', encoding='utf-8') as file:
        token  = file.read()
    headers={'Authorization': f'Token {token}'}
    json = {
        "id": 11,
        "quantity": 5
    }
    response = requests.put("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
    assert response.text == '{"отказ":"У вас нет такого товара в корзине"}'


### КОРЗИНА - изменить количество товара который уже оплачен &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# def test_26_put_paid_order(buyer1):
#    with open(buyer1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    json = {
#        "id": 11,
#        "quantity": 5
#    }
#    response = requests.put("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
#    assert response.text == '{"отказ":"Заказ уже оплачен и перемещен из корзины"}'


### КОРЗИНА - удалить товар по его id
# def test_27_delete_order(buyer1):
#    with open(buyer1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    response = requests.delete("http://127.0.0.1:8000/orderitem/?id=6", headers=headers)
#    assert response.text == '{"успех":"Товар удалён из корзины"}'


### КОРЗИНА - удалить товар по его id (неверный id)
def test_28_delete_order_by_id(buyer1):
    with open(buyer1, 'r', encoding='utf-8') as file:
        token  = file.read()
    headers={'Authorization': f'Token {token}'}
    response = requests.delete("http://127.0.0.1:8000/orderitem/?id=7", headers=headers)
    assert response.text == '{"отказ":"В корзине нет товара с таким id"}'


### КОРЗИНА - удалить оплаченный товар (неверный id) &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# def test_29_delete_order_by_id(buyer1):
#    with open(buyer1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    response = requests.delete("http://127.0.0.1:8000/orderitem/?id=7", headers=headers)
#    assert response.text == '{"отказ":"Заказ уже оплачен и перемещен из корзины"}'


### КОРЗИНА - удалить товар по его id с неверным токеном
def test_30_delete_order_by_id(buyer1):
    invalid_token={'Authorization': 'Token ee5550f707475e92a1c151e6a75eb61a6ecabd'}
    response = requests.delete("http://127.0.0.1:8000/orderitem/?id=7", headers=invalid_token)
    assert response.text == '{"detail":"Invalid token."}'


### ЗАКАЗ - Посмотреть все заказы
def test_31_get_list_order(buyer1):
    with open(buyer1, 'r', encoding='utf-8') as file:
        token  = file.read()
    headers={'Authorization': f'Token {token}'}
    response = requests.get("http://127.0.0.1:8000/order/", headers=headers)
    assert response.status_code == 200


### Создать заказ(ордер)
#def test_32_create_order(buyer1):
#    with open(buyer1, 'r', encoding='utf-8') as file:
#        token  = file.read()
#    headers={'Authorization': f'Token {token}'}
#    response = requests.post("http://127.0.0.1:8000/order/?id=1", headers=headers)
#    assert response.status_code == 200
