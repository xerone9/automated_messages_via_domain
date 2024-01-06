import os
import csv
from checking_new_emails_with_conditions import CheckingNewEmails
from decrypting_files import DecryptingFiles
from send_email import SendEmail


def is_11_rows(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        # Count the number of rows (excluding header)
        num_rows = sum(1 for row in reader)
    return num_rows == 11


def main():
    data_dict = {
        "Account_Number": [],
        "Account_Name": [],
        "Available_Balance": [],
    }
    check_email = CheckingNewEmails()

    # sending that attachment for evaluation
    if len(check_email) > 0:
        decryption = DecryptingFiles(check_email)
        # if decryption done
        if len(decryption) > 0:
            for file in decryption:
                if file[2]:
                    SendEmail(file[0], file[1], file[3])
                else:
                    print(f'{file[0]} - Password Not Found')
                    os.remove(str(file[0]).replace("unlocked - ", ""))

            csv_file_path = next(file for file in os.listdir() if file.endswith(".csv"))
            if csv_file_path:
                if is_11_rows(csv_file_path):
                    # If true, perform the operation
                    with open(csv_file_path, 'r') as file:
                        reader = csv.DictReader(file)
                        # Iterate over rows and append values to the dictionary
                        for row in reader:
                            data_dict["Account_Number"].append(row["Account Number"])
                            data_dict["Account_Name"].append(row["Account Name"])
                            data_dict["Available_Balance"].append(row["Available Balance"])
                        temp_variable = None

                    # adding totol line
                    # Convert available balance values to float and calculate the total
                    total_balance = 0.0

                    for i in range(len(data_dict["Available_Balance"])):
                        try:
                            balance_float = float(data_dict["Available_Balance"][i].replace(',', ''))
                            total_balance += balance_float
                        except ValueError:
                            total_balance = 0.0
                            data_dict["Account_Number"].append("")
                            data_dict["Account_Name"].append("")
                            data_dict["Available_Balance"].append("can't process")
                            break

                    # Append the total balance to the "Available_Balance" list
                    if total_balance != 0.0:
                        data_dict["Available_Balance"].append(f'{total_balance:,.2f}')
                        data_dict["Account_Number"].append("")
                        data_dict["Account_Name"].append("")

                    SendEmail(temp_variable, "Available Balance in Accounts Dated: " + csv_file_path.split(".csv")[0], data_dict)
        else:
            print("No Statement with Password Found")


if __name__ == "__main__":
    main()
