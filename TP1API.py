import requests
from datetime import datetime, timedelta

# Volume quotidien moyen du BTC et de l'ETH en USDT, USDC, USD et EUR

for j in ['bitcoin', 'ethereum']:
    url = f'https://api.coingecko.com/api/v3/coins/{j}/tickers'
    response = requests.get(url)
    data_q1 = response.json()
    for i in ['USDT', 'USDC', 'USD', 'EUR']:
        if 'tickers' in data_q1:
            tickers = data_q1['tickers']
            tickers_filtre = [ticker['volume'] for ticker in tickers if ticker['target']==i]
            volume = sum([volume for volume in tickers_filtre])
            print(f'{j} avg daily volume in {i} is {volume}{i}')
        else:
            print('Tickers not found')

# Même donnée pour les 10 cryptomonnaies les plus liquides après BTC et ETH
import requests
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en"
response = requests.get(url)
data = response.json()
coins = [coin for coin in data if coin['id'] not in ['bitcoin', 'ethereum']][:10]
volumes = {coin['id']: {'USD':0, 'EUR':0, 'USDT':0, 'USDC':0} for coin in coins}
for i in volumes:
    url = f'https://api.coingecko.com/api/v3/coins/{i}/tickers'
    response = requests.get(url)
    data = response.json()
    for j in ['USDT', 'USDC', 'USD', 'EUR']:
        tickers = data['tickers']
        filtre = [ticker for ticker in tickers if ticker['target'] == j]
        volumes[i][j] = sum([ticker['volume'] for ticker in filtre])

for coin_id, volume_data in volumes.items():
    print(f"{coin_id}: {volume_data}")

# Top 3 des cryptomonnaies les plus liquides contre BTC et ETH comme devises de cotation,
# avec volume
import requests
from collections import defaultdict

volumes = defaultdict(float)
base_currencies = ['bitcoin', 'ethereum']

for base in base_currencies:
    url = f'https://api.coingecko.com/api/v3/coins/{base}/tickers'
    response = requests.get(url)
    data = response.json()
    tickers = data.get('tickers', [])

    for ticker in tickers:
        base = ticker['base'].lower()
        target = ticker['target'].lower()

        if target in ['btc', 'eth'] and base not in ['btc', 'eth']:
            volume = ticker['converted_volume'][target]
            volumes[base] += volume

sorted_cryptos = sorted(volumes.items(), key=lambda x: x[1], reverse=True)[:3]
top_cryptos = [{'crypto': crypto, 'volume': volume} for crypto, volume in sorted_cryptos]
print(top_cryptos)

# 4. Top 3 des stablecoins les plus liquides comme devises de cotation, avec volume

import requests
import pandas as pd

stablecoins = ['usdt', 'usdc', 'tusd', 'dai', 'pax', 'busd', 'ust', 'sUSD']
tickers_dataframes = []

for stablecoin in stablecoins:
    url = f'https://api.coingecko.com/api/v3/coins/{stablecoin}/tickers'
    response = requests.get(url)
    tickers = response.json().get('tickers', [])
    tickers_df = pd.DataFrame(tickers)
    tickers_dataframes.append(tickers_df)

df = pd.concat(tickers_dataframes, ignore_index=True)
df['target'] = df['target'].str.lower()
df = df[df['target'].isin(stablecoins)]
df['volume'] = df.apply(lambda x: x['converted_volume'].get(x['target'], 0), axis=1)
volume_by_stablecoin = df.groupby('target')['volume'].sum().sort_values(ascending=False)
top_stablecoins = volume_by_stablecoin.head(4).reset_index()
top_stablecoins.columns = ['Stablecoin', 'Total Volume']
print(top_stablecoins)
