import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apikey import cmc_key
api_key = cmc_key
Fiat_currency = 'USD'
coin_symbol = 'SOL'


# Set the high and low price thresholds for alerts
high_point = 145
low_point = 100

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Parameters for the API request: which cryptocurrency to get the price for and in which fiat currency
parameters = {
    'symbol': coin_symbol,
    'convert': Fiat_currency
}

headers = {
    'X-CMC_PRO_API_KEY': api_key
}
# Function to fetch the current price of the cryptocurrency from CoinMarketCap API
def get_price():

    response = requests.get(url, headers=headers, params=parameters)
    
    # Ensure the request was successful and check the price of the specified coin
    if response.status_code == 200:
        data = response.json()
        price = data['data'][coin_symbol]['quote'][Fiat_currency]['price']
        return price
    else:
        return f"Error: {response.status_code}, {response.text}"

# price = get_price()
# print(price)


# Function to send an email notification with a subject and message
def send_email(subject, message):
     # Sender's Outlook email and password (for authentication)
    sender_email = 'testcoinmarketcap@outlook.com'
    recipient_email = 'umi.naomij@gmail.com'
    sender_password = 'Coinmark!123'
    
    
    # Setup the email using MIME (Multipurpose Internet Mail Extensions) for formatting
    msg = MIMEMultipart()
    msg['From']=sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    #attach plain text to the email
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Create an SMTP session to connect to Outlook's SMTP server
        server = smtplib.SMTP('smtp.office365.com', 587) 
        # Start TLS encryption for security
        server.starttls()
        # Log in to the SMTP server using the sender's email credentials
        server.login(sender_email, sender_password)
        # Convert the email (MIME message) into a string
        text = msg.as_string()
        # Send the email to the recipient
        server.sendmail(sender_email, recipient_email, text)
        # Terminate the SMTP session
        server.quit()
        print(f'The email has b een sent to {recipient_email}')
    except Exception as e:
        print(f'Email failed to send: {e}')
        
        
# Function to check the current price of the cryptocurrency and send alerts
def check_price():
    current_price = get_price()
    print(f'{coin_symbol} price is {current_price}')
    
    if current_price >= high_point:
        subject = f'{coin_symbol} Price Alert: High Point Reached'
        message = f'The current price of {coin_symbol} is ${current_price}. This price is above or equal to the high point of ${high_point}.'
        send_email(subject, message)
        print(f'{coin_symbol} has reached a high price of ${current_price}')
        
    elif current_price <= low_point:
        subject = f'{coin_symbol} Price Alert: Low Point Reached'
        message = f'The current price of {coin_symbol} is ${current_price}. This price is below or equal to the low point of ${low_point}.'
        send_email(subject, message)
        print(f'{coin_symbol} has reached a high price of ${current_price}')
        
check_price()

