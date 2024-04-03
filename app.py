from flask import Flask, render_template, jsonify
import requests
from threading import Thread
import time
import json

app = Flask(__name__)

data_file_path = 'data.json'

def fetch_trade_data_for_mint(mint):
    url = f"https://client-api.pump.fun/trades/{mint}?limit=200&offset=0"
    response = requests.get(url)
    if response.status_code == 200:
        trades = response.json()
        for trade in trades:
            if trade['user'] == "specific_user_id" and not trade['is_buy']:
                return True
    return False

def update_data_cache_with_rugged_info(data_cache):
    for coin in data_cache:
        coin['rugged'] = fetch_trade_data_for_mint(coin['mint'])

def fetch_data():
    url = "https://client-api.pump.fun/coins?offset=0&limit=50&sort=last_trade_timestamp&order=DESC&includeNsfw=true"
    response = requests.get(url)
    data_cache = []
    if response.status_code == 200:
        data_cache = response.json()
        update_data_cache_with_rugged_info(data_cache)
        with open(data_file_path, 'w') as data_file:
            json.dump(data_cache, data_file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/api/data')
def api_data():
    with open(data_file_path, 'r') as data_file:
        data = json.load(data_file)
    return jsonify(data)



def fetch_and_update_data():
    while True:
        fetch_data()  # Your existing function to fetch the main coin data
        time.sleep(0.2)  # Example: Adjust based on your rate limit and needs

if __name__ == '__main__':
    # Replace direct calls to fetch_data() with fetch_and_update_data()
    Thread(target=fetch_and_update_data, daemon=True).start()
    app.run(debug=True)