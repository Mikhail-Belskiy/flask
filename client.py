from http.client import responses
import requests

# Пример создания объявления
advert_data = {
    "title": "Объявление1",
    "description": "Описание объявления",
    "owner_id": "777"
}

# Создание объявления
response = requests.post('http://127.0.0.1:5000/api/v1/adverts', json=advert_data)
print(response.json())  # Вывод результата создания объявления

# Получение списка всех объявлений
response = requests.get('http://127.0.0.1:5000/api/v1/adverts')
print(response.json())  # Вывод всех объявлений

# Получение конкретного объявления (предположим, с ID 1)
response = requests.get('http://127.0.0.1:5000/api/v1/adverts/1')
print(response.json())  # Вывод конкретного объявления
