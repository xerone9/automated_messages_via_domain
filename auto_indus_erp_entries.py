from PyPDF2 import PdfReader
from datetime import datetime
import os
import cx_Oracle


def convert_date(input_date):
    # Parse the input date string
    parsed_date = datetime.strptime(input_date, '%d-%b-%Y')

    # Format the date into the desired format
    formatted_date = parsed_date.strftime('%Y-%m-%d')

    return formatted_date


def read_pdf(file):
    pdf_file = file
    vouchers = []
    reader = PdfReader(pdf_file)
    pages = len(reader.pages)
    for i in range(pages):
        page = reader.pages[i]
        page_text = str(page.extract_text()).split("\n")
        for line in page_text:
            if line.__contains__('CASH DEPOSIT'):
                words = line.split(" ")
                CASH_DEPOSIT_index = words.index('CASH')
                if len(line.split(" ")[CASH_DEPOSIT_index - 1]) >= 3:
                    try:
                        vouchers.append(int(line.split(" ")[CASH_DEPOSIT_index - 1]))
                    except Exception as e:
                        pass

    vouchers = list(dict.fromkeys(vouchers))
    return vouchers


def sql_working(vouchers, date):
    table_name = 'Request_for_posting'
    sql_query = f"INSERT INTO {table_name} (posting_date, voucher_no) VALUES_TO_INSERT"
    value = ""
    if len(vouchers) > 0:
        for voucher in vouchers:
            value += f"SELECT DATE '{convert_date(date)}', {voucher} FROM dual UNION ALL "
        value = value[:-11]
        sql_query = sql_query.replace('VALUES_TO_INSERT', value)
        return sql_query
    else:
        return None


def connect_and_pass_sql(sql_code):
    if sql_code:
        os.environ['PATH'] = 'C:/oracle/instantclient_19_3;' + os.environ['PATH']

        # print("LD_LIBRARY_PATH:", os.environ.get('LD_LIBRARY_PATH'))
        print("PATH:", os.environ.get('PATH'))

        # Replace these with your actual values
        username = ''
        password = ''
        ip = ''
        port = '1521'  # Default Oracle port is 1521
        connect_string = ''

        os.environ['PATH'] = 'C:/oracle/instantclient_19_3;' + os.environ['PATH']

        # Construct the connection string
        dsn = cx_Oracle.makedsn(ip, port, service_name=connect_string)

        # Establish the connection
        connection = cx_Oracle.connect(username, password, dsn)

        # Create a cursor
        cursor = connection.cursor()

        cursor.execute(sql_code)
        connection.commit()

        # cursor.execute("SELECT * FROM request_for_posting")
        # result = cursor.fetchall()
        # for row in result:
        #     print(row)

        # Don't forget to close the cursor and connection when you're done
        cursor.close()
        connection.close()


def make_entry_in_erp(file, date):
    filter_date = str(date.split(" - ")[1])
    vouchers = read_pdf(file)
    sql_insert_code = sql_working(vouchers, filter_date)
    connect_and_pass_sql(sql_insert_code)