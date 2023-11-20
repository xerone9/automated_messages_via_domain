import datetime
import requests
import sys
import os
from checking_new_emails_with_conditions import CheckingNewEmails
from decrypting_files import DecryptingFiles
from send_email import SendEmail

datex = str(datetime.datetime.now()).split(".")
date_and_time = str(datex[0]).split(" ")
date = date_and_time[0]
time = date_and_time[1]

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    message = 'Process Started...\n\n' + time + '\nYou can now close this page'
    start_response(status, headers)
    return [message.encode()]
    

def main():
    check_email = CheckingNewEmails()

    # sending that attachment for evaluation
    if len(check_email) > 0:
        decryption = DecryptingFiles(check_email)
        # if decryption done
        if len(decryption) > 0:
            statement_summary = decryption[-1]
            for file in decryption:
                if not isinstance(file, dict):
                    if file[2]:
                        SendEmail(file[0], file[1], statement_summary)
                    else:
                        print(f'{file[0]} - Password Not Found')
                        os.remove(str(file[0]).replace("unlocked - ", ""))
        else:
            print("No Statement with Password Found")

with open('limit_reload.ini', 'r') as f:
    for line in f:
        limit_reload = line


if str(time).split(":")[0] + ":" + str(time).split(":")[1] != limit_reload:
    with open('limit_reload.ini', 'w') as file:
        file.write(str(time).split(":")[0] + ":" + str(time).split(":")[1])
    main()
    sys.exit(0)
    
    