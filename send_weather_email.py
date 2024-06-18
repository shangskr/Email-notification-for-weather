import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Get environment variables
CITY = os.getenv('CITY')
API_KEY = os.getenv('API_KEY')

# Check if CITY and API_KEY are defined
if not CITY or not API_KEY:
    raise ValueError('CITY or API_KEY environment variables are not defined.')

# OpenWeatherMap API endpoint
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    # Fetching weather data from OpenWeatherMap
    response = requests.get(url)
    data = response.json()

    # Extracting relevant weather information
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']

    # Email content
    subject = f"Weather Report for {CITY}"
    body = f"Current weather in {CITY}:<br><br>" \
           f"Weather: {weather_description}<br>" \
           f"Temperature: {temperature}°C<br>" \
           f"Humidity: {humidity}%"

    # Email configuration
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not receiver_email or not password:
        raise ValueError('SENDER_EMAIL, RECEIVER_EMAIL, or EMAIL_PASSWORD environment variables are not defined.')

    # Sending email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.example.com', 587) as server:  # Update with your SMTP server details
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
except Exception as e:
    print(f'Failed to send email. Error: {str(e)}')
