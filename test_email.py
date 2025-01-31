import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = '[email]'
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('[email]', '[password]')
            server.send_message(msg)
            print("Email sikeresen elküldve Gmail-en keresztül.")
    except Exception as e:
        print("Hiba történt az email küldése közben:", e)


# Teszteljük az email küldést
send_email('[email]', 'Teszt Email', 'Ez egy teszt email.')
