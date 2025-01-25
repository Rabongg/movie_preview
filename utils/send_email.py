import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_email(movie_info_list):
    load_dotenv()
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465  # SSL 포트
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_KEY')
    
    recipient_email = os.getenv('RECEIVER_EMAIL')
    subject = 'Test Email from Python via Google SMTP'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(make_body_pretty(movie_info_list), 'html'))
    
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')

def make_body_pretty(movie_info_list):
    html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>영화 정보</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
                .container { max-width: 600px; margin: auto; background-color: white; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { background-color: #4CAF50; color: white; padding: 15px; text-align: center; border-radius: 5px 5px 0 0; }
                .movie { border-bottom: 1px solid #ccc; padding: 15px; }
                .movie:last-child { border-bottom: none; }
                .title { font-size: 18px; font-weight: bold; }
                .date { color: #555; }
                .cinemas { margin-top: 5px; }
                .cinema { background-color: #f1f1f1; padding: 5px; border-radius: 3px; display: inline-block; margin-right: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>영화 정보</h1>
                </div>
                <div class="content">
        """
    
    for movie in movie_info_list:
        html_content += f"""
            <div class="movie">
                <div class="title">{movie[0]}</div>
                <div class="date">상영 기한: {movie[1]}</div>
                <div class="cinemas">
                    <strong>영화관: {movie[2]}</strong>
                </div>
            </div>
        """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content