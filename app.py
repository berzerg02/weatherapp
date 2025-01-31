from flask import Flask, render_template, request, flash
import requests
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Szükséges a flash üzenetekhez

# API kulcs betöltése környezeti változóból vagy alapértelmezett érték
API_KEY = os.getenv('WEATHER_API_KEY', '[API-key]')  # Cseréld le a saját API kulcsodra

def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = '[email]'  # Feladó email
    msg['To'] = recipient  # Címzett email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # SMTP kapcsolat Gmail-en keresztül
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('[email]', '[pswd]')  # Alkalmazásjelszó
            server.send_message(msg)
            print("Email sikeresen elküldve.")
    except Exception as e:
        print(f"Hiba történt az email küldése közben: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        recipient_email = request.form.get('email')

        if not city or not recipient_email:
            flash('Kérjük, adja meg a város nevét és az email címet.', 'danger')
        else:
            # Adatgyűjtés az API-ból
            url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no'
            response = requests.get(url)
            data = response.json()

            if 'error' in data:
                flash(f"Hiba: {data['error']['message']}", 'danger')
            else:
                weather = {
                    'city': data['location']['name'],
                    'country': data['location']['country'],
                    'temp_c': data['current']['temp_c'],
                    'condition': data['current']['condition']['text'],
                    'icon': data['current']['condition']['icon']
                }

                # Email tartalom előkészítése
                subject = f"Időjárás Jelentés: {weather['city']}"
                body = (f"Város: {weather['city']}, {weather['country']}\n"
                        f"Hőmérséklet: {weather['temp_c']} °C\n"
                        f"Állapot: {weather['condition']}")

                # Email küldése
                send_email(recipient_email, subject, body)
                flash(f"Az időjárás jelentés elküldve a(z) {recipient_email} címre.", 'success')

    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
