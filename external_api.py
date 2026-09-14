import requests

user_id = input("Enter user ID: ")

url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

response = requests.get(url)

if response.status_code == 200:
    user = response.json()

    print("Name:", user["name"])
    print("Email:", user["email"])
    print("City:", user["address"]["city"])
    print("--------------------")
else:
    print("API request failed.")
    print("Status code:", response.status_code)