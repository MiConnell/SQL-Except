import sys

try:
    import pandas as pd
except ImportError as e:
    print(
        "Oops! something is missing, please install by typing `pip install pandas` and report back!"
    )
    sys.exit(1)
try:
    import pyodbc
except ImportError as e:
    print(
        "Oops! There is no SQL driver installed, please install by typing `pip install pyodbc` and report back!"
    )
    sys.exit(1)
try:
    from Credentials import conn, cursor
except ImportError as e:
    server = input("Server Name: ")
    database = input("Database: ")
    auth = input("Use Windows Credentials? y/n ")
    if auth in ["n", "N"]:
        user = input("Username: ")
        password = input("Password: ")
        conn = pyodbc.connect(
            r"DRIVER=SQL Server;"
            fr"SERVER={server};"
            fr"fDATABASE={database};"
            fr"UID={user};"
            fr"PWD={password};"
        )
        save_credentials = input(
            "Would you like to save these credentials for next time? y/n"
        )
        if save_credentials in ["y", "Y"]:
            print(
                "This is awkward...I didn't think you'd say yes. I haven't figured out how to do that yet..."
            )
    else:
        conn = pyodbc.connect(
            r"DRIVER=SQL Server;"
            fr"SERVER={server};"
            fr"DATABASE={database};"
            r"Trusted_Connection=yes;"
        )


def Main():
    table = input("Which table would you like to select from? ")
    exclude = input(
        "Which columns would you like to exclude? Enter a list separated by spaces: "
    ).split()
    conditions = input("Do you have any conditions? y/n ")
    conditions = (
        input("Enter your WHERE clause here: WHERE ")
        if conditions in ["y", "Y"]
        else "1 = 1"
    )
    results = generate_sql_query(table, exclude, conditions)
    print(results)
    check = input("Do you have another query you'd like to generate? ")
    Main() if check in ["y", "Y"] else input("Thank you 😊😊 have a nice day 😎")


def generate_sql_query(table, exclude, where):
    all_columns = f"""
    --sql
        SELECT
        COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table}'
        AND COLUMN_NAME NOT IN ('{"', '".join(map(str, [e for e in exclude]))}');
    """
    df = pd.read_sql(all_columns, conn)
    lst = ", ".join(map(str, [c for c in df["column_name"]]))
    return f"""
    SELECT {lst} FROM {table} where {where};
    """


if __name__ == "__main__":
    Main()
