import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        if 'message' in data:
            raise Exception(f"Error fetching weather data: {data['message']}")
        else:
            raise Exception("Unknown error fetching weather data")
    elif data.get("cod") == "404":
        raise Exception(f"City '{city}' not found")

    return data

def send_email(weather_data, sender_email, receiver_email, password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Daily Weather Forecast"

    try:
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        wind_direction = weather_data["wind"]["deg"]
        sunrise_timestamp = weather_data["sys"]["sunrise"]
        sunset_timestamp = weather_data["sys"]["sunset"]
        sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except KeyError as e:
        raise Exception(f"Missing expected weather data in response: {e}")

    body = f"""
    Hello!

    This is the daily weather forecast for {weather_data.get('name', 'your city')}:

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
        print(f"Connecting to SMTP server...")
        server = smtplib.SMTP("smtp.office365.com", 587)  # SMTP服务器地址和端口
        server.starttls()
        print(f"Logging in as {sender_email}...")
        server.login(sender_email, password)
        print(f"Sending email to {receiver_email}...")
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    city = os.getenv("CITY")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")

    try:
        print(f"Fetching weather data for {city}...")
        weather_data = get_weather(api_key, city)
        print("Weather data fetched successfully!")
        send_email(weather_data, sender_email, receiver_email, email_password)
    except Exception as e:
        print(f"Error: {e}")
