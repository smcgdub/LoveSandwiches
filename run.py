import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers seperated 
    by commas. The loop will repeatedly request data, until the data is valid.
    """
    while True:
        print("1. Please enter sales data from the last market")
        print("2. Data should be six sets of numbers seperated by commas")
        print("3. Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid.")
            break

    return sales_data
    
    
def validate_data(values):
    """
    Inside the try converts all string values to intergers.
    Raises ValueError if strings cannot be converted into 
    integers or if there's not exactly six values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
              f"exactly 6 values are required you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales workshett...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updates successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra was made when sold out.
    """
    print("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    #pprint(stock)
    #stock_row = SHEET.worksheet("stock").row_values(9)
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to love sandwiches data automation.\n")
main()
