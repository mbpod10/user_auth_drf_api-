from urllib import response
import requests


def client():
    token = 'Token 6494df2e0b986bade0cee256fd8f375810bb4678'
    # url = 'http://127.0.0.1:8000/api/rest-auth/login/'
    url = 'http://127.0.0.1:8000/api/profiles/'
    # payload = {
    #     "username": "brock",
    #     "password": "123"
    # }

    # response = requests.post(url=url, data=payload)
    headers = {
        'Authorization': token
    }
    response = requests.get(url=url, headers=headers)
    return response.json()


print(client())
