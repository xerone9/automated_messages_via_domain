import smtplib
import os
from email.message import EmailMessage


def SendEmail(file, account_number_and_date):
    sender_email = ''
    receiver_email = 'bankstatement@indus.edu.pk'
    smtp_server = 'cpanel-s90.web-hosting.com'
    port = 465
    login = ''
    password = ''

    message = EmailMessage()
    message['Subject'] = f'Unlocked Statement - {account_number_and_date}'
    message['From'] = f'Askari Bank Statements <{sender_email}>'
    message['To'] = receiver_email
    content = 'Respected Sir,\n\nFind The Attachments\n\nRegards,\nUsman Mustafa Khawar'
    message.set_content(content)

    with open(file, 'rb') as f:
        file_data = f.read()
        # print(file.split("\\")[-1])
        message.add_attachment(file_data, maintype='application', subtype='pdf', filename=file)

    # Connect to the SMTP server and send the message
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(login, password)
        server.send_message(message)

    os.remove(file)
    print('Email sent successfully!')
