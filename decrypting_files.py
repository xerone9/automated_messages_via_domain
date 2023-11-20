import os
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter


passwords = []

with open("passwords.ini") as file:
    data = file.readlines()
    for line in data:
        values = str(line.strip())
        passwords.append(values)


def DecryptingFiles(encrypted_files):
    decrypted_files = []
    account_number = ""
    statement_date = ""
    for encrypted_file in encrypted_files:
        file_unlocked = True
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
                        account_number = ""
                        statement_date = ""
                        opening_balance = "0.00"
                        closing_balance = "0.00"
                        total_deposits = "0.00"
                        clearing_amount = "0.00"
                        total_withdrawals = "0.00"
                        for i in range(pages):
                            page = reader.pages[i]
                            information = str(page.extract_text())
                            try:
                                if information.__contains__("Pak Rupees"):
                                    account_number = information.split("Pak Rupees")[1].split(" Account #")[0]
                                    if statement_date == "":
                                        statement_date = information.split(" ** Closing Balance **")[0][-11:]
                                    if statement_date.__contains__("DB"):
                                        statement_date = information.split(" ** Opening Balance ** ")[1].split("Value Date")[0]
                                    opening_balance = information.split(" ** Opening Balance **")[0].split("Time Balance Date\n")[1]
                                    closing_balance = information.split("\nIMPORTANT INFORMATION")[0].split(" ")[-1]
                                    total_deposits = information.split(" TOTAL DEPOSITS  ")[1].split("  ")[1]
                                    clearing_amount = information.split(" ** Closing Available Balance **")[1].split("\n")[0]
                                    total_withdrawals = information.split(" TOTAL DEPOSITS  ")[1].split("  ")[2].split(" ")[0]

                                    os.rename(str(decrypted_file), account_number + " - " + statement_date + ".pdf")
                                    decrypted_file = account_number + " - " + statement_date + ".pdf"
                            except Exception as errors:
                                print(errors)
                        statement_summary = {
                            'Opening_Balance': opening_balance,
                            'Total_Deposits': total_deposits,
                            'Total_Withdrawals': total_withdrawals,
                            'Clearing_Amount': clearing_amount,
                            'Available_Balance': closing_balance,
                        }
                        break
                else:
                    # print("No Password Found For: " + encrypted_file)
                    file_unlocked = False
            else:
                pass

        decrypted_files.append([decrypted_file, account_number + " - " + statement_date, file_unlocked])
        decrypted_files.append(statement_summary)

    return decrypted_files
