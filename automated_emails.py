import os
from checking_new_emails_with_conditions import CheckingNewEmails
from decrypting_files import DecryptingFiles
from send_email import SendEmail


# Checking New Emails: Came From accountofficer@indus.edu.pk
def main():
    check_email = CheckingNewEmails()

    # sending that attachment for evaluation
    if len(check_email) > 0:
        decryption = DecryptingFiles(check_email)
        # if decryption done
        if len(decryption) > 0:
            for file in decryption:
                if file[2]:
                    SendEmail(file[0], file[1])
                else:
                    print(f'{file[0]} - Password Not Found')
                    os.remove(str(file[0]).replace("unlocked - ", ""))
        else:
            print("No Statement with Password Found")


if __name__ == "__main__":
    main()
