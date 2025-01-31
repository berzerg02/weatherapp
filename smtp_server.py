import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('Beérkezett üzenet:')
        print('Feladó:', mailfrom)
        print('Címzettek:', rcpttos)
        print('Üzenet:')
        print(data)
        print('---')
        # Itt további feldolgozást végezhetsz, például az üzenetek mentését

if __name__ == '__main__':
    server = CustomSMTPServer(('localhost', 1025), None)
    print('SMTP szerver fut a 1025-ös porton...')
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print('SMTP szerver leállítva.')
