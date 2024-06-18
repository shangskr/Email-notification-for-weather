# send_weather_email.py

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def send_email(weather_data):
    sender_email = "your_email@example.com"  # 发件人邮箱
    receiver_email = "recipient_email@example.com"  # 收件人邮箱
    password = "your_email_password"  # 发件人邮箱密码或授权码

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Daily Weather Forecast"

    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    wind_direction = weather_data["wind"]["deg"]
    sunrise_timestamp = weather_data["sys"]["sunrise"]
    sunset_timestamp = weather_data["sys"]["sunset"]
    sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime("%Y-%m-%d %H:%M:%S")

    body = f"""
    Hello!

    This is the daily weather forecast for Xingtai:

    Weather: {weather_description}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    Wind Speed: {wind_speed} m/s
    Wind Direction: {wind_direction}°
    Sunrise Time: {sunrise_time}
    Sunset Time: {sunset_time}

    This email was sent automatically by a script.
    """

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)  # SMTP服务器地址和端口
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    api_key = "2a3c49fab5cfe490bb5bb9df0b4d3877"
    city = "Xingtai"
    weather_data = get_weather(api_key, city)
    send_email(weather_data)
