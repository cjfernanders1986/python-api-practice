import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print(response.status_code)

users = response.json()

 
print("Users in Gwenborough:")

for user in users:
    if user["address"]["city"] == "Gwenborough":
        print("Name:", user["name"])
        print("Email:", user["email"])