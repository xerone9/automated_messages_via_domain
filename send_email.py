import smtplib
import os
from email.message import EmailMessage


def SendEmail(file, account_number_and_date, statement_summary):
    sender_email = ''
    receiver_email = ''
    smtp_server = 'cpanel-s90.web-hosting.com'
    port = 465
    login = ''
    password = ''

    message = EmailMessage()
    message['Subject'] = f'Unlocked Statement - {account_number_and_date}'
    message['From'] = f'Askari Bank Statements <{sender_email}>'
    message['To'] = receiver_email

    formatted_keys = [key.replace('_', ' ') for key in statement_summary.keys()]

    table_html = '<table border="1" style="border-collapse: collapse; width: 100%;">'

    # Header row with styling
    table_html += '<tr style="background-color: black; color: white; text-align: center; font-weight: bold;">'
    for formatted_key in formatted_keys:
        table_html += f'<td>{formatted_key}</td>'
    table_html += '</tr>'

    # Values row with styling
    table_html += '<tr style="background-color: white; color: black; text-align: center;">'
    for value in statement_summary.values():
        table_html += f'<td>{value}</td>'
    table_html += '</tr>'

    table_html += '</table>'

    # Email content with the table
    content = f'''
    Respected Sir,

    <div style="margin-top: 10px;">
        Below is the summary of Account:<br>
        {table_html}
    </div>
    <div style="font-style: italic; color: red; font-size: small; font-weight: bold;">
        Alert!!! Bot translations can be inaccurate. Kindly confirm before proceeding with the values.
    </div>
    <div style="font-style: italic; color: green; font-size: small;">
        Above information may be sent on Whatsapp as well.
    </div>

    <div style="margin-top: 10px;">
        Find The Attachments
    </div>

    <div style="margin-top: 10px; font-size: small;">
        Regards,<br>
        <span style="font-weight: bold;">Usman Mustafa Khawar</span>
    </div>
    <div style="font-style: italic; color: grey; font-size: small;">
        This is an automated email via personal domain.
    </div>
    '''
    message.set_content(content, subtype='html')  # Set content subtype to 'html' for HTML content

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
