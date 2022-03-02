import requests


def client():
    url = 'http://127.0.0.1:8000/api/rest-auth/regisration/'
    data = {
        'username': 'mitzy101',
        'email': 'mitz@gmail.com',
        'password1': 'testpass1@',
        'password2': 'testpass1@'
    }
    response = requests.post(url=url, data=data)
    print(response.json())


def retrieve_profiles():
    url = 'http://127.0.0.1:8000/api/profiles/'
    headers = {
        'Authorization': 'Token be31cd319b46c08c4d4b976111bba74976afc46a'
    }
    response = requests.get(url=url, headers=headers)
    print(response.json())


if __name__ == '__main__':
    # client()
    retrieve_profiles()
