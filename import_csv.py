"""
Load CSV file(s) and add transactions to EveryDollar
"""

from everydollar_api import EveryDollarAPI
from datetime import datetime
import csv, sys

try:
    from creds import username, password
except ImportError:
    print("Please create a creds.py file with the variables username and password defined with your everydollar credentials")
    print("")
    print("example creds.py: ")
    print("username = \"my username\"")
    print("password = \"my password\"")
    sys.exit()

# Initialize variables
# Modify dateFmt to match format of dates in your CSV
#  Year - %Y is 4 digit, %y is 2 digit
#  Month, day - %m, %d
#  Hour - %H in 24 hour clock, %I is 12 hour clock
#  Minute - %M
#  Second - %S
dateFmt = "%m/%d/%Y" #03/24/2023
# Column names
HEADERS = {"date": "Post Date",
           "exp": "Debit",
           "inc": "Credit",
           "desc": "Description"
          }
filenames = ['transactions.csv']
totalTx = 0

api = EveryDollarAPI()
api.login(username, password)

if len(sys.argv) > 1:
    filenames = sys.argv[1:]

print("Sending transactions to EveryDollar")
for file in filenames:
    with open(file, newline='') as csvfile:
        filereader = csv.DictReader(csvfile, delimiter=',')
        TxCount = 0
        
        for row in filereader:
            info = {"Amt": float(row[HEADERS['inc']]) if row[HEADERS['inc']] != "" else float(f"-{row[HEADERS['exp']]}"),
                    "Date": datetime.strptime(row[HEADERS['date']], dateFmt),
                    "Desc": row[HEADERS['desc']]
                   }
            api.add_transaction(info["Date"], info["Desc"], abs(info["Amt"]), "expense" if info["Amt"] < 0 else "income")
            TxCount += 1
        
        totalTx += TxCount
        if len(sys.argv) > 2:
            print(f"Processed {TxCount} transactions from {file}")

print(f"Added {totalTx} transactions. Now for the fun part!")
