import time


def get_symbols():
    import requests
    url = "https://data-api.binance.vision/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [d['symbol'] for d in data['symbols'] if d['status']=='TRADING']
    return symbols

import requests
import pandas as pd

def candle_data(symbol_list):
    all_data = {}
    for symbol in symbol_list[:10]:
        url = "https://data-api.binance.vision/api/v3/uiKlines"
        params = {
            'symbol': symbol,
            'interval': '1m',
            'limit': 60
        }
        response = requests.get(url, params=params)
        data = response.json()
        close_prices = [price[5] for price in data]
        all_data[symbol]=close_prices
    combined_df = pd.DataFrame(all_data)
    return combined_df

symbols = get_symbols()
print(candle_data(symbols))

# 3. Méthodes d'exécution
############################# Asynchrone ###############################
import asyncio
import aiohttp
import time

async def get_symbols():
    async with aiohttp.ClientSession() as session:
        url = "https://data-api.binance.vision/api/v3/exchangeInfo"
        async with session.get(url) as response:
            data = await response.json()
            symbols = [d['symbol'] for d in data['symbols'] if d['status']=='TRADING']
            return symbols

async def candle_data(symbol, session):
        url = "https://data-api.binance.vision/api/v3/uiKlines"
        params = {
            'symbol': symbol,
            'interval': '1m',
            'limit': 60
        }
        async with session.get(url, params=params) as response:
            data = await response.json()
            close_prices = [price[5] for price in data]
            return symbol, close_prices

async def get_data_candle(symbols_list):
    async with aiohttp.ClientSession() as session:
        tasks = [candle_data(symbol, session) for symbol in symbols_list]
        responses = await asyncio.gather(*tasks)
        return responses

async def main():
    symbols = await get_symbols()
    data_candle = await get_data_candle(symbols[:10])
    print(data_candle)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    temps_asynchrone = time.time() - start
    print(temps_asynchrone)

######################### Multithreading #########################################
import requests
import threading
import pandas as pd

# Fonction pour récupérer la liste des symboles de trading de Binance
def get_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    return [d['symbol'] for d in data['symbols'] if d['status'] == 'TRADING']

# Fonction utilisée dans un thread unique pour chaque symbole
# La fonction prend en args un dictionnaire vide et le renvoie avec les données
def get_candle_data(symbol, data_dict):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': '1m',
        'limit': 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Stocke les close price pour chaque symbole dans le dic
    data_dict[symbol] = [float(price[4]) for price in data]

# Fonction main pour organiser le multithreading
def main():
    symbols = get_symbols()[:10]  # Appelle de get_symbols pour 10 symboles
    threads = []
    candle_data = {}

    # Création et démarrage des threads
    for symbol in symbols:
        # Chaque thread exécute la fonction get_candle_data pour un symbole
        # Si la fonction utilisé par target a besoin d'args => args=(symbol, candle_data)
        thread = threading.Thread(target=get_candle_data, args=(symbol, candle_data))
        thread.start()  # Démarre l'exécution du thread
        threads.append(thread)

    # Attendre que tous les threads soient terminés
    for thread in threads:
        thread.join()  # Attend que le thread soit terminé

    # Conversion des données récupérées en DataFrame pandas
    candle_data_df = pd.DataFrame(candle_data)
    print(candle_data_df)

# Exécuter le programme si le script est le point d'entrée principal
if __name__ == "__main__":
    main()

############################## MULTIPROCESSING ##################################""
import requests
import multiprocessing
import pandas as pd

def get_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    return [d['symbol'] for d in data['symbols'] if d['status'] == 'TRADING']

def get_candle_data(symbol, data_queue):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': '1m',
        'limit': 60
    }
    response = requests.get(url, params=params)
    data = response.json()
    # La méthode .put() est utilisée avec l'objet Queue dans le module multiprocessing de Python.
    # Elle permet de placer un élément dans la queue. Ici on ajoute un tuple à la queue : symbol et son close price
    data_queue.put((symbol, [float(price[4]) for price in data]))

# Fonction main qui organise multiprocessing
def main():
    symbols = get_symbols()[:10]
    # Utilisation d'une queue pour collecter les données des processus
    data_queue = multiprocessing.Queue()
    processes = []

    # Création et démarrage des processus
    for symbol in symbols:
        process = multiprocessing.Process(target=get_candle_data, args=(symbol, data_queue))
        process.start()
        processes.append(process)

    # Attendre que tous les processus soient terminés
    for process in processes:
        process.join()

    # Récupérer les données de la queue et les stocker dans un dictionnaire
    candle_data = {}
    while not data_queue.empty():
        symbol, data = data_queue.get()
        candle_data[symbol] = data

    # Conversion des données en DataFrame
    candle_data_df = pd.DataFrame(candle_data)
    print(candle_data_df)

if __name__ == "__main__":
    main()

######################## WEBSOCKET ##################################
# recevoir les mises à jour du carnet
# d'ordres de niveau 1 toutes les 100 ms.
import websockets
import asyncio
import json

async def get_data(symbols):
    streams = '/'.join([symbol + '@depth@100ms' for symbol in symbols])
    url = f"wss://stream.binance.com:9443/stream?streams={streams}"
    print(url)
    async with websockets.connect(url) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)


if __name__ == "__main__":
    symbols = ["btcbnb"]
    asyncio.run(get_data(symbols))


async def compare_ba(symbol):
    await ge

