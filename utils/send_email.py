import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_email():
    load_dotenv()
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465  # SSL 포트
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_KEY')
    
    recipient_email = os.getenv('RECEIVER_EMAIL')
    subject = 'Test Email from Python via Google SMTP'
    body = 'This is a test email sent from a Python script using Google SMTP.'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')