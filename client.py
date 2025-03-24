import requests


headers={'Authorization': 'Token 3fe97506c6c86f7d3250b1e50cd81e5e484a645c'}


### регистрация пользователя
#json = {
#    "username": "jt1",
#    "password": "user1",
#    "first_name": "E1",
#    "last_name": "T1",
#    "email": "dylan_jt@mail.ru"
#}
#response = requests.post("http://127.0.0.1:8000/user/register/", json=json)


### получить список пользователей
#response = requests.get("http://127.0.0.1:8000/user/")
#print(response.text)


### вход пользователя в акаунт
#json = {
#    "email": "delan_jt@mail.ru",
#    "password": "user"
#}
#response = requests.post("http://localhost:8000/user/login/", json=json)
#print(response.text)


### создать магазин
#json = {
#           "name": "Test",
#           "url": "https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml"
#       }
#response = requests.post("http://localhost:8000/shop/", json=json)


### Посмотреть список магазинов
#response = requests.get("http://127.0.0.1:8000/shop/")
#print(response.status_code)
#print(response.text)


### обновление магазина
#json = {
#    "name": "Пятёрочка",
#    "url": "www.piatorochka.ru"
#}
#response = requests.post("http://localhost:8000/up/", json=json)


### посмотреть содержание корзины
#response = requests.get("http://127.0.0.1:8000/basket/")
#print(response.status_code)
#print(response.text)


### ЗАКАЗ - добавить товары
#json = {"add_products":
#    [
#        {
#            "product_info": 46,#1
#            "shop": 8,#2
#            "quantity": 1
#        },
#        {
#            "product_info": 54,#10
#            "shop": 8,#2
#            "quantity": 1
#        }
#    ]
#}
#response = requests.post("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
#print(response.status_code)
#print(response.text)


### ТОВАР - изменить количество товара по его id
json = {
    "id": 9,
    "quantity": 188
}
response = requests.put("http://127.0.0.1:8000/orderitem/", json=json, headers=headers)
print('-----', response.status_code)
print('-----', response.text)






### Посмотреть все ордеры заказ(ордер)
#response = requests.get("http://127.0.0.1:8000/order/",
#                         headers={'Authorization': 'Token 797d0e1ed5229ee6bcbc408becb5c31a50d889c1'}
#                        )
#print(response.status_code)
#print(response.text)
#

### Создать заказ(ордер)
#response = requests.post("http://127.0.0.1:8000/order/?id=3",
#                         headers={'Authorization': 'Token 797d0e1ed5229ee6bcbc408becb5c31a50d889c1'}
#                        )
#print(response.status_code)
#print(response.text)
