import smtplib
import os
from email.message import EmailMessage
from email.mime.image import MIMEImage
import time
from auto_indus_erp_entries import make_entry_in_erp


def SendEmail(file, account_number_and_date, statement_summary):
    sender_email = ''
    receiver_email = 'accountofficer-2@indus.edu.pk'
    smtp_server = 'cpanel-s90.web-hosting.com'
    port = 465
    login = ''
    password = ''

    if not file:
        # New statement order has been set and 2 accounts removed by Kamran Sir
        # total_balance = float(str(statement_summary['Available_Balance'][-1]).replace(",", ""))
        # index_number_212 = statement_summary['Account_Number'].index('0861480800212')
        # index_number_66 = statement_summary['Account_Number'].index('0860380800066')
        # negate_212_balance = float(str(statement_summary['Available_Balance'][index_number_212]).replace(",", ""))
        # negate_66_balance = float(str(statement_summary['Available_Balance'][index_number_66]).replace(",", ""))
        # new_balance = total_balance - negate_212_balance - negate_66_balance

        statement_order = ['0861480800100',
                           '0861480800336',
                           '0861480800085',
                           '0861480800507',
                           '0861480800074',
                           '0860380800055',
                           '0861480800041',
                           '0861480800405',
                           '0861480800391',
                           ''] # As per Kamran Sir

        statement_summary_2 = {
            'Account_Number': [],
            'Account_Name': [],
            'Available_Balance': []
        }

        for order in statement_order:
            order_index = statement_summary['Account_Number'].index(order)
            statement_summary_2['Account_Number'].append(statement_summary['Account_Number'][order_index])
            statement_summary_2['Account_Name'].append(statement_summary['Account_Name'][order_index])
            # statement_summary_2['Available_Balance'].append(statement_summary['Available_Balance'][order_index])
            balance_in_integers = int(float(str(statement_summary['Available_Balance'][order_index]).replace(",", "")))
            statement_summary_2['Available_Balance'].append(balance_in_integers)

        statement_summary_2['Available_Balance'].pop()

        new_balance = 0
        for balances in statement_summary_2['Available_Balance']:
            new_balance += balances

        balance_with_commas = []
        for balance in statement_summary_2['Available_Balance']:
            balance_with_commas.append(f'{balance:,}')

        statement_summary_2['Available_Balance'] = balance_with_commas


        statement_summary_2['Available_Balance'].append(f'{new_balance:,}')
        statement_summary = statement_summary_2

    message = EmailMessage()
    if file:
        message['Subject'] = f'Unlocked Statement - {account_number_and_date}'
    else:
        time.sleep(10)
        message['Subject'] = account_number_and_date

    message['From'] = f'Askari Bank Statements <{sender_email}>'
    message['To'] = receiver_email

    formatted_keys = [key.replace('_', ' ') for key in statement_summary.keys()]

    if file:
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
    else:
        table_html = '<table border="1" style="border-collapse: collapse;">'

        # Header row with styling
        table_html += '<tr style="background-color: black; color: white; text-align: center; font-weight: bold;">'
        for formatted_key in formatted_keys:
            # Set text-align to left for all columns
            table_html += f'<td style="padding-left: 5px; text-align: left; width: 1px">{formatted_key}</td>'

        table_html += '</tr>'

        # Values rows with styling
        for i in range(10):  # Assuming there are 9 + 1 (Total) values in each list
            # Determine background color based on odd or even row
            background_color = 'white' if i % 2 == 0 else '#f2f2f2'
            color = 'black'
            if i == 9:
                background_color = 'black'
                color = 'white'

            table_html += f'<tr style="background-color: {background_color}; color: {color}; text-align: left;">'
            for key in statement_summary.keys():
                if key == "Account_Number":
                    value = statement_summary[key][i]
                    table_html += f'<td style="padding-left: 5px; width: 150px;">{value}</td>'
                elif key == "Account_Name":
                    value = statement_summary[key][i]
                    table_html += f'<td style="padding-left: 5px; width: 575px;">{value}</td>'
                elif key == "Available_Balance":
                    value = statement_summary[key][i]
                    table_html += f'<td style="padding-right: 5px; width: 150px; text-align: right;">{value}</td>'
            table_html += '</tr>'

        table_html += '</table>'

    if file:
        remarks = "Below is the summary of Account"
    else:
        remarks = "Available Balance In Accounts Today"

    content = f'''
        Respected Sir,

        <div style="margin-top: 10px;">
            {remarks}:<br><br>
            {table_html}
        </div>
        <div style="color: red; font-size: small; font-weight: bold;">
            Alert!!! Bot translations can be inaccurate. Kindly confirm before proceeding with the values.
        </div>
        <div style="font-style: italic; color: green; font-size: small;">
            Above information may be sent on Whatsapp as well.
        </div>

        <div style="margin-top: 10px;">
            Find The Attachments
        </div>

        <div style="margin-top: 10px; font-size: small;">
            <br>Regards,<br>
            <img src="cid:Usman_Sign3" alt="Animated GIF3" style="width: 25%; height: auto;"><br>
            <span style="font-weight: bold;">Usman Mustafa Khawar</span><br>
            <span style="">Automation Specialist</span><br>
            <a href="https://github.com/xerone9" style="text-decoration: none; color: #000000;">
                <img src="cid:git_logo" alt="YouTube Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-botton: 2px;">
            </a>
            <a href="https://www.linkedin.com/in/usman-mustafa-khawar-41374a234/" style="text-decoration: none; color: #000000;">
                <img src="cid:linkedin_logo" alt="YouTube Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-botton: 2px;">
            </a>
            <a href="https://softwares.rubick.org/" style="text-decoration: none; color: #000000;">
                <img src="cid:web_logo" alt="YouTube Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-botton: 2px;">
            </a>
            <a href="https://www.upwork.com/freelancers/~01e2b4984cd54db890" style="text-decoration: none; color: #000000;">
                <img src="cid:upwork_logo" alt="YouTube Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-botton: 2px;">
            </a>
            <a href="https://www.youtube.com/channel/UCbczhEOorBjQUwFbkUG9AGg" style="text-decoration: none; color: #000000;">
                <img src="cid:youtube_logo" alt="YouTube Icon" style="width: 20px; height: 20px; vertical-align: middle; margin-botton: 2px;">
            </a>
        </div>
        <div style="font-style: italic; color: grey; font-size: small;">
            This is an automated email via private domain.
        </div>
        '''

    # Set content as an alternative to the multipart
    message.add_alternative(content, subtype='html')

    # Attach the inline images
    for image_name in ['Usman_Sign3.gif', 'git_logo.png', "linkedin_logo.png", "web_logo.png", "upwork_logo.png", "youtube_logo.png"]:
        with open(image_name, 'rb') as image_file:
            image_data = image_file.read()
            image_cid = f"<{image_name.split('.')[0]}>"

            # Create a new MIMEImage part for each image
            image_part = MIMEImage(image_data, name=image_name)
            image_part.add_header('Content-ID', image_cid)
            image_part.add_header('Content-Disposition', 'inline')
            message.attach(image_part)

    if file:
        with open(file, 'rb') as f:
            file_data = f.read()
            message.add_attachment(file_data, maintype='application', subtype='pdf', filename=file)

    # Connect to the SMTP server and send the message
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(login, password)
        server.send_message(message)

    if file:
        os.remove(file)
    else:
        existing_csv_files = [file for file in os.listdir() if file.endswith(".csv")]

        for file in existing_csv_files:
            os.remove(file)

    print('Email sent successfully!')



