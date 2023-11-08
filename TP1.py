import requests

# 3.1)
response = requests.get("https://api.publicapis.org/entries")
data = response.json()
for entry in data['entries'][:10]:
    print(entry['API'], "-", entry['Description'])

response = requests.get("https://api.publicapis.org/entries?category=Finance")
finance_data = response.json()
for entry in finance_data['entries'][:10]:
    print(entry['API'], "-", entry['Description'])

# 3.2)
url = "https://api.coingecko.com/api/v3/coins/list"
response = requests.get(url)
coins = response.json()
for coin in coins[:10]:
    print(coin["id"], "-", coin["name"])

coin_id = "bitcoin"
detailed_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
detailed_response = requests.get(detailed_url)
coin_details = detailed_response.json()

print(coin_details['name'])
print("Valeur actuelle:", coin_details["market_data"]["current_price"]["usd"], "USD")

# 3.3)
coin_id = "bitcoin"
volume_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=5"

response = requests.get(volume_url)
data = response.json()
print(data)
