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
                        for i in range(pages):
                            page = reader.pages[i]
                            information = str(page.extract_text())
                            try:
                                if information.__contains__("Pak Rupees"):
                                    account_number = information.split("Pak Rupees")[1].split(" Account #")[0]
                                    statement_date = information.split(" ** Closing Balance **")[0][-11:]
                                    if statement_date.__contains__("DB"):
                                        statement_date = information.split(" ** Opening Balance ** ")[1].split("Value Date")[0]
                                    os.rename(str(decrypted_file), account_number + " - " + statement_date + ".pdf")
                                    decrypted_file = account_number + " - " + statement_date + ".pdf"
                                    break
                            except Exception as errors:
                                print(errors)
                        break
                else:
                    # print("No Password Found For: " + encrypted_file)
                    file_unlocked = False
            else:
                pass

        decrypted_files.append([decrypted_file, account_number + " - " + statement_date, file_unlocked])

    return decrypted_files
