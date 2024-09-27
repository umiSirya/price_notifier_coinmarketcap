import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

#load environment variables from the .env file
load_dotenv()

# Function to send an email notification with a subject and message
def send_email(subject, message):
     # Sender's Outlook email and password (for authentication)
    sender_email = os.getenv('email')
    recipient_email = 'umi.naomij@gmail.com'
    sender_password = os.getenv('sender_email_password')
    
    
    # Setup the email using MIME (Multipurpose Internet Mail Extensions) for formatting
    msg = MIMEMultipart()
    msg['From']=sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    #attach plain text to the email
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Create an SMTP session to connect to Outlook's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587) 
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