import logging
import requests
from datetime import datetime
import azure.functions as func

app = func.FunctionApp()

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
SHEETDB_API_URL = "https://sheetdb.io/api/v1/arlnfmrmn4uys"

def fetch_crypto_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(COINGECKO_URL, params=params)
    response.raise_for_status()
    return response.json()

def analyze_data(data):
    top5 = sorted(data, key=lambda x: x['market_cap'], reverse=True)[:5]
    avg_price = sum(coin['current_price'] for coin in data) / len(data)
    changes = [coin['price_change_percentage_24h'] for coin in data]
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'top5': top5,
        'avg_price': avg_price,
        'max_change': max(changes),
        'min_change': min(changes)
    }

def generate_report(analysis):
    report = f"""Cryptocurrency Analysis Report ({analysis['timestamp']})

Top 5 Cryptocurrencies by Market Cap:
"""
    for idx, coin in enumerate(analysis['top5'], 1):
        report += f"{idx}. {coin['name']} ({coin['symbol'].upper()}): ${coin['market_cap']:,.2f}\n"

    report += f"""
Average Price (Top 50): ${analysis['avg_price']:,.2f}
24h Change Range: {analysis['min_change']:.2f}% to {analysis['max_change']:.2f}%
"""
    with open('/tmp/crypto_report.txt', 'w') as f:
        f.write(report)

def update_sheetdb(data):
    sheet_data = [{
        "Name": coin['name'],
        "Symbol": coin['symbol'].upper(),
        "Price (USD)": coin['current_price'],
        "Market Cap (USD)": coin['market_cap'],
        "24h Volume (USD)": coin['total_volume'],
        "24h Price Change (%)": coin['price_change_percentage_24h']
    } for coin in data]

    logging.info("Data being sent to SheetDB: %s", sheet_data)

    requests.delete(f"{SHEETDB_API_URL}/all")
    response = requests.post(SHEETDB_API_URL, json=sheet_data)
    response.raise_for_status()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    
    try:
        data = fetch_crypto_data()
        analysis = analyze_data(data)
        generate_report(analysis)
        update_sheetdb(data)
        logging.info('Update successful at %s', datetime.now())
    except Exception as e:
        logging.error('Error: %s', str(e))