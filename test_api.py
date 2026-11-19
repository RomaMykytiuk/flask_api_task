
import requests

URL = "http://127.0.0.1:5000"

# Створюємо тестового студента
response = requests.post(
    f"{URL}/students",
    json={
        "first_name": "API",
        "last_name": "Test",
        "group_id": 1
    }
)

student_id = response.json()["id"]
print("CREATE:", response.status_code)

# Оновлюємо ім'я
response = requests.put(
    f"{URL}/students/{student_id}",
    json={"first_name": "Updated"}
)

print("UPDATE:", response.status_code)
print(response.json())

# Видаляємо тестового студента
response = requests.delete(f"{URL}/students/{student_id}")
print("DELETE:", response.status_code)
