import os
import csv
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

passwords = []

account_translation = {
    "0860380800066": 'INDUS UNIVERSITY (EX) P.N.B.M.D.C FOUNDATION',
    "0860380800055": 'INDUS UNIVERSITY (PNBMDCF) CONFERENCE',
    "0861480800041": 'INDUS INST OF HIGH EDU PNBMDC',
    "0861480800074": 'INDUS UNIVERSITY(SCHOLARSHIP) PNBMDC FOUNDATION',
    "0861480800212": 'KHALID AMIN SHEIKH',
    "0861480800085": 'INDUS UNIVERSITY.(TECHNOLOGY) PNBMDC FOUNDATION',
    "0861480800405": 'S.B.B CITY UNI (PROJECT) OF T',
    "0861480800336": 'INDUS UNIVERSITY (PROJECT OF P',
    "0861480800391": 'THE NATIONAL EDUCATION FOUNDATION',
    "0861480800507": 'INDUS UNIVERSITY(DEGREE)PROJECT OF PNBMDC FOUNDATION',
    "0861480800100": 'P.N.B.M.D.C (PAKISTAN NATIONAL BUILDING MATARIAL DISPLAY CENTRE FOUNDATION)'
}

with open("passwords.ini") as file:
    data = file.readlines()
    for line in data:
        values = str(line.strip())
        passwords.append(values)


def DecryptingFiles(encrypted_files):
    decrypted_files = []
    for encrypted_file in encrypted_files:
        file_unlocked = True
        statement_date = ""
        account_number = ""
        opening_balance = "0.00"
        closing_balance = "0.00"
        total_deposits = "0.00"
        clearing_amount = "0.00"
        total_withdrawals = "0.00"
        decrypted_file = "unlocked - " + encrypted_file
        # reader = PdfReader(desktop + filename)
        with open(encrypted_file, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            if pdf_reader.is_encrypted:
                # Loop through each password and try to decrypt the file
                for password in passwords:
                    if pdf_reader.decrypt(password) == 1:

                        # If the password is correct, create a new PDF file without password
                        pdf_writer = PdfWriter()
                        for page_num in range(len(pdf_reader.pages)):
                            pdf_writer.add_page(pdf_reader.pages[page_num])
                        with open(decrypted_file, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        pdf_reader.stream.close()
                        os.remove(encrypted_file)
                        reader = PdfReader(decrypted_file)
                        pages = len(reader.pages)
                        for i in range(pages):
                            page = reader.pages[i]
                            information = str(page.extract_text())
                            if information.__contains__("Pak Rupees"):
                                if i == 0:
                                    if account_number == "":
                                        account_number = information.split("Pak Rupees")[1].split(" Account #")[0]
                                    if statement_date == "":
                                        statement_date = information.split(" ** Closing Balance **")[0][-11:]
                                    if statement_date.__contains__("DB"):
                                        statement_date = information.split(" ** Opening Balance ** ")[1].split("Value Date")[0]
                                    try:
                                        if opening_balance == "0.00":
                                            opening_balance = information.split(" ** Opening Balance **")[0].split("Time Balance Date\n")[1]
                                    except IndexError:
                                        if opening_balance == "0.00":
                                            opening_balance = "Un-readable"
                                try:
                                    if closing_balance == "0.00":
                                        closing_balance = information.split("** Closing Available Balance **")[1].split("\n")[1].replace(" ", "")
                                except IndexError:
                                    if pages == i - 1:
                                        if closing_balance == "0.00":
                                            closing_balance = "Un-readable"
                                try:
                                    if total_deposits == "0.00":
                                        total_deposits = information.split(" TOTAL DEPOSITS  ")[1].split("  ")[1]
                                except IndexError:
                                    if pages == i - 1:
                                        if total_deposits == "0.00":
                                            total_deposits = "Un-readable"
                                try:
                                    if clearing_amount == "0.00":
                                        clearing_amount = information.split(" ** Closing Available Balance **")[1].split("\n")[0]
                                except IndexError:
                                    if pages == i - 1:
                                        if clearing_amount == "0.00":
                                            clearing_amount = "Un-readable"
                                try:
                                    if total_withdrawals == "0.00":
                                        total_withdrawals = information.split(" TOTAL DEPOSITS  ")[1].split("  ")[2].split(" ")[0]
                                except IndexError:
                                    if pages == i - 1:
                                        if total_withdrawals == "0.00":
                                            total_withdrawals = "Un-readable"

                        os.rename(str(decrypted_file), account_number + " - " + statement_date + ".pdf")
                        decrypted_file = account_number + " - " + statement_date + ".pdf"
                        statement_summary = {
                            'Opening_Balance': opening_balance,
                            'Total_Deposits': total_deposits,
                            'Total_Withdrawals': total_withdrawals,
                            'Clearing_Amount': clearing_amount,
                            'Available_Balance': closing_balance,
                        }
                        decrypted_files.append(
                            [decrypted_file, account_number + " - " + statement_date, file_unlocked, statement_summary])

                        existing_csv_files = [file for file in os.listdir() if file.endswith(".csv")]

                        for file in existing_csv_files:
                            if file != f"{statement_date}.csv":
                                os.remove(file)
                                print(f"Deleted: {file}")

                        csv_file_path = f"{statement_date}.csv"
                        if not os.path.exists(csv_file_path):
                            with open(csv_file_path, 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["Account Name", "Account Number", "Available Balance"])

                        with open(csv_file_path, 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([account_translation[account_number], account_number, closing_balance])

                        break
                else:
                    print("No Password Found For: " + encrypted_file)
                    file_unlocked = False
            else:
                pass

    return decrypted_files
