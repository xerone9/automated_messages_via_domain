import imaplib
import email


def CheckingNewEmails():
    imap_server = 'cpanel-s90.web-hosting.com'
    username = ''
    password = ''

    # Connect to the IMAP server
    with imaplib.IMAP4_SSL(imap_server) as server:
        # Login to the server
        server.login(username, password)

        # Select the mailbox
        server.select('inbox')

        # Search for unread emails in the mailbox
        _, message_numbers = server.search(None, 'UNSEEN')

        # Print the list of unread emails
        # print(f"List of Unread Emails:")
        encrypted_files = []
        for num in reversed(message_numbers[0].split()):
            _, msg_data = server.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            print(email_message['Date'])
            # if str(email_message['Date']).__contains__("2023"):
            #     print(f"\t{email_message['From']} - {email_message['Subject']} - {email_message['Date']}")
            #     # server.store(num, '+FLAGS', '\\Seen')
            if email_message['From'] == '"' + "'Askari Bank Limited' via Bank Statement" + '" <bankstatement@indus.edu.pk>':
                pass
            else:
                print(f"\t{email_message['From']} - {email_message['Subject']} - {email_message['Date']}")
                if str(email_message['Subject']).__contains__("Unlocked"):
                    server.store(num, '+FLAGS', '\\Seen')
                else:
                    if email_message.is_multipart():
                        content = ''
                        attachments = []
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain':
                                content += part.get_payload(decode=True).decode()
                            elif content_type == 'application/pdf' or content_type == 'application/octet-stream' or content_type == 'application/x-pdf' or content_type == 'image/jpeg':
                                attachment = {}
                                attachment['filename'] = part.get_filename()
                                attachment['content'] = part.get_payload(decode=True)
                                attachments.append(attachment)
                    else:
                        content = email_message.get_payload(decode=True).decode()
                    email_message.set_payload(content)

                    if attachments:
                        print(f"Attachments:")
                        for attachment in attachments:
                            print(f" - {attachment['filename']}")

                            # Save the attachment to disk
                            with open(attachment['filename'], 'wb') as f:
                                f.write(attachment['content'])
                            print(f" - Downloaded to {attachment['filename']}")

                            encrypted_file = attachment['filename']
                            if encrypted_file not in encrypted_files:
                                encrypted_files.append(encrypted_file)
                    else:
                        pass

    return encrypted_files