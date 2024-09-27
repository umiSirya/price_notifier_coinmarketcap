import requests
from emailalert import send_email
import os
from dotenv import load_dotenv
import csv


# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv('cmc_key')
Fiat_currency = 'USD'

# Function to fetch the top 200 coins of the cryptocurrency from CoinMarketCap API
def get_top_200_coins():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  

    # Parameters for the API request to get top 200 coins
    parameters = {
        'start': 1,
        'limit': 200,
        'convert': Fiat_currency
    }

    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }

    response = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        crypto_coins = response.json()
        coins = crypto_coins['data']
        return coins       
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to check the current price of the cryptocurrency and send alerts
def check_price(coin_symbol, high_point, low_point):
    coins = get_top_200_coins()
    specific_coin = next((coin for coin in coins if coin['symbol'] == coin_symbol), None)

    if specific_coin:  # Check if the coin exists
        current_price = specific_coin['quote'][Fiat_currency]['price']  # Extract the price
        print(f'{coin_symbol} price is ${current_price}')

        if current_price >= high_point:
            subject = f'{coin_symbol} Price Alert: High Point Reached'
            message = f'The current price of {coin_symbol} is ${current_price}. This price is above or equal to the high point of ${high_point}.'
            send_email(subject, message)
            print(f'{coin_symbol} has reached a high price of ${current_price}')
            
        elif current_price <= low_point:
            subject = f'{coin_symbol} Price Alert: Low Point Reached'
            message = f'The current price of {coin_symbol} is ${current_price}. This price is below or equal to the low point of ${low_point}.'
            send_email(subject, message)
            print(f'{coin_symbol} has reached a low price of ${current_price}')
    else:
        print(f'{coin_symbol} not found in the top 200 coins.')

# Function to write top 200 coins data to CSV
def write_to_csv():    
    coins = get_top_200_coins()  
    
    with open('crypto_coins.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Position', 'Name', 'Symbol', 'Price'])
        
        for index, coin in enumerate(coins, start=1):
            name = coin['name']
            symbol = coin['symbol']
            price = coin['quote'][Fiat_currency]['price']
            writer.writerow([index, name, symbol, price])

# Main program flow to get inputs from the user and run the check_price function
def main():
    # Take user input for coin symbol and price thresholds
    coin_symbol = input("Enter the cryptocurrency symbol (e.g., BTC, ETH, SOL): ").upper()
    high_point = float(input(f"Enter the high price alert for {coin_symbol}: "))
    low_point = float(input(f"Enter the low price alert for {coin_symbol}: "))

    print("\nChecking prices and sending alerts if necessary...\n")
    check_price(coin_symbol, high_point, low_point)
    
    # Ask if the user wants to export data to CSV
    export_csv = input("Do you want to export the top 200 coins data to CSV? (yes/no): ").lower()

    if export_csv == 'yes':
        write_to_csv()
        print("\nData exported to crypto_coins.csv")

if __name__ == '__main__':
    main()
