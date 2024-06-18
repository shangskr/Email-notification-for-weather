import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# OpenWeatherMap API endpoint
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Fetching weather data from OpenWeatherMap
try:
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
    sender_email = SENDER_EMAIL
    receiver_email = RECEIVER_EMAIL
    password = EMAIL_PASSWORD

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
