import requests

username = input("Enter GitHub username: ")

url = f"https://api.github.com/users/{username}"

response = requests.get(url)

if response.status_code == 200:
    user = response.json()

    print("Username:", user["login"])
    print("Name:", user["name"])
    print("Public repos:", user["public_repos"])
    print("Followers:", user["followers"])
    print("Following:", user["following"])
    print("Profile:", user["html_url"])

else:
    print("GitHub user not found.")
    print("Status code:", response.status_code)