import pytest

# from rest_framework.test import APIClient

import requests


#@pytest.fixture
#def client():
#    return APIClient()

@pytest.fixture
def user_registration_json():
    json = {
        "username": "user_test_api_pytest",
        "password": "8ae341e3f8a2c92b98d6a90f66384621ffe6",
        "email": "dylan_jt@mail.ru",
        "mail_confirmation_code": "2071"
    }
    return json

@pytest.fixture
def token():
    # user_id = User.objects.get(username='user_test_api_pytest').id
    with open('tests/backend/token_user_test_api_pytest.txt', 'r', encoding='utf-8') as file:
        token  = file.read()
    return token


# @pytest.fixture
# def user_json():
#    json = {
#        "email": "test@mail.ru",
#        "password": "user1"
#    }
#    return json

# def import_data():
#     assert True

### Удалить пользователя
def test_1_user_delete(token):
    headers={'Authorization': f'Token {token}'}
    json = {
        "username": "user_test_api_pytest"
    }
    response = requests.delete("http://127.0.0.1:8000/user/", json=json, headers=headers)
    print(response.status_code)
    assert response.text == '{"успех":"Пользователь удалён"}'


### регистрация без имени пользователя
def test_2_create_user_no_user_name():
   json = {"password": "8ae341e3f8a2c92b98d6a90f66384621ffe6", "email": "test@mail.ru"}
   response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
   assert response.text == '{"отказ":"Имя пользователя не указано"}'


### регистрация без пороля
def test_3_create_user_no_password():
   json = {"username": "test_user_0", "email": "dylan_jt@mail.ru"}
   response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
   assert response.text == '{"отказ":"Пароль не указан"}'


### регистрация пользователя без почты
def test_4_create_user_no_email():
   json = {"username": "test_user_0", "password": "8ae341e3f8a2c92b98d6a90f66384621ffe6"}
   response = requests.post("http://127.0.0.1:8000/user/register/", json=json)
   assert response.text == '{"отказ":"Email не указан"}'


### регистрация пользователя
def test_5_create_user(user_registration_json):
    response = requests.post("http://127.0.0.1:8000/user/register/", json=user_registration_json)
    assert response.text == '{"успех":"Регистрация выполнена"}'


### регистрация пользователя с занятым именем
def test_6_create_user_with_taken_name(user_registration_json):
   response = requests.post("http://127.0.0.1:8000/user/register/", json=user_registration_json)
   assert response.text == '{"отказ":"Имя пользователя занято"}'


### получить список пользователей
def test_7_get_list_user():
   response = requests.get("http://127.0.0.1:8000/user/")
   assert response.status_code == 200


### вход пользователя c неверным логином или паролем
def test_8_user_login_folse():
   json = {"email": "tteesstt@mail.ru", "password": "user1"}
   response = requests.post("http://localhost:8000/user/login/", json=json)
   assert response.text == '{"отказ":"Неверный логин или пароль"}'


### вход пользователя
def test_9_user_login(user_registration_json):
   response = requests.post("http://localhost:8000/user/login/", json=user_registration_json)
   assert response.text == '{"успех":"Вход в выполнен."}'



    

# создать магазин с неверным токеном
#def test_create_shop_invalid_token():
#    #Arrange
#    invalid_token={'Authorization': 'Token ee55150f707475e92a1c151e6a75eb61a6ecabd'}
#    json = {
#               "name": " Связной_test",
#               "url": "www.связной.ру"
#           }
#    #Act
#    response = requests.post("http://localhost:8000/shop/", json=json, headers=invalid_token)
#    #Assert
#    assert response.text == '{"detail":"Invalid token."}'
#
# создать магазин с верным токеном
#def test_create_shop_correct_token():
#    #Arrange
#    token={'Authorization': 'Token 2ee55150f707475e92a1c151e6a75eb61a6ecabd'}
#
#    json = {
#               "name": " Связной_test16",
#               "url": "www.связной.ру"
#           }
#    #Act
#    response = requests.post("http://localhost:8000/shop/", json=json, headers=token)
#    #Assert
#    assert response.text == '{"успех":"Магазин создан"}'
#
#
# Магазин с таким названием уже существует
#def test_create_shop_with_a_taken_name():
#    #Arrange
#    token={'Authorization': 'Token 2ee55150f707475e92a1c151e6a75eb61a6ecabd'}
#
#    json = {
#               "name": " Связной_test16",
#               "url": "www.связной.ру"
#           }
#    #Act
#    response = requests.post("http://localhost:8000/shop/", json=json, headers=token)
#    #Assert
#    assert response.text == '{"отказ":"Магазин с таким названием уже существует"}'
#
#
# Заполнены не все обязательные поля
#def test_create_shop_with_not_all_fields_filled_in():
#    #Arrange
#    token={'Authorization': 'Token 2ee55150f707475e92a1c151e6a75eb61a6ecabd'}
#
#    json = {
#               "name": " Связной_test17",
#           }
#    #Act
#    response = requests.post("http://localhost:8000/shop/", json=json, headers=token)
#    #Assert
#    assert response.text == '{"отказ":"Заполнены не все обязательные поля"}'


























