import requests

url = "http://127.0.0.1:8000/data-collection/upload"
headers = {
    "X-API-KEY": "supersecretapikey",
    "Content-Type": "application/json"
}
data = [
    {
        "name": "Organic Milk 1L",
        "brand": "BrandX",
        "type": "Milk",
        "size": "1L",
        "upc": "1234567890123",
        "keywords": "organic, milk, dairy",
        "price": 3.99,
        "sale_price": 2.99,
        "is_on_sale": True,
        "sale_start": "2024-06-01T00:00:00",
        "sale_end": "2024-06-07T23:59:59",
        "store_name": "Supermarket A",
        "store_location": "123 Main St",
        "api_source": "aqcia.ge",
        "quantity": 20,
        "last_restocked": "2024-06-01T08:00:00"
    }
]

response = requests.post(url, json=data, headers=headers)
print("Status code:", response.status_code)
print("Response:", response.json()) 