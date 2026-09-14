import requests

country = input("Enter a country: ")

url = f"https://api.restcountries.com/countries/v5?q={country}"

headers = {
    "Authorization": "Bearer rc_live_demo"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
if response.status_code == 200:
    data = response.json()

    country_data = data["data"]["objects"][0]

    print("Country:", country_data["names"]["common"])
    print("Capital:", country_data["capitals"][0]["name"])
    print("Region:", country_data["region"])
    print("Population:", f'{country_data["population"]:,}')

else:
    print("API request failed.")
    print("Status code:", response.status_code)