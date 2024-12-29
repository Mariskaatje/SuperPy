# Imports
import argparse
import csv
import datetime

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():
    pass

# Vaststellen welke dag het is.

today = datetime.date.today()
print(f'Datum: {today}')

# Van datetime naar string  

datetime_to_string = today.strftime('%Y-%m-%d')

print(f'Het is vandaag {datetime_to_string}')

# Van string naar datetime

# string_to_datetime = datetime.datetime.strptime(today_string, '%Y_%m_%d')
# print(string_to_datetime)

# Vooruit zetten van de datum

from datetime import datetime, timedelta
#today_date = datetime.date.today()

while True:  
    datum_vooruit = input('Wilt u de datum vooruit zetten? (ja/nee): ').strip().lower()
    if datum_vooruit == "nee":
       break
    elif datum_vooruit == 'ja':
       number = int(input('Hoeveel dagen wilt u de datum vooruit zetten?'))
       today_date = datetime.now()
       date_after_number_days = today_date + timedelta(days=number)
       print(f'De datum na {number} dagen is: {date_after_number_days.strftime("%Y-%m-%d")}')
       if number == 1:
          print(f'Over 1 dag is het {date_after_number_days}')
       else:
          print(f'Over {number} dagen is het {date_after_number_days}')
    else:
       print("Ongeldige invoer, probeer het opnieuw.")   

# products.csv

# Invoer van productgegevens

products = []
while True:
    id = input('Voer de id in ')
    product_name = input('Voer de product_name in ')
    bought_date = input('Voer de bought_date (YYYY-MM-DD) in ')
    bought_price = float(input('Voer de bought_price in '))
    expiration_date = input('Voer de expiration_date in (YYYY-MM-DD)')
    sell_date = input('Voer de sell_date (YYYY-MM-DD) in ')
        
    if today >= expiration_date:
       sell_price = 'expired'
       print("The item is no longer available for sale.")

from datetime import datetime

def check_item_availability(expiration_date_str, today_str=None):
    """
    Checks if an item is available for sale based on its expiration date.

    :param expiration_date_str: The expiration date in 'YYYY-MM-DD' format.
    :param today_str: (Optional) The current date in 'YYYY-MM-DD' format. Defaults to today's date.
    :return: A tuple (status, message), where status is either 'available' or 'expired'.
    """
    try:
        # Parse the expiration date
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
        
        # Use today's date if not provided
        today = datetime.strptime(today_str, "%Y-%m-%d").date() if today_str else datetime.today().date()
        
        # Check the item's availability
        if today >= expiration_date:
            return 'expired', "The item is no longer available for sale."
        else:
            return 'available', "The item is still available for sale."
    
    except ValueError as e:
        return 'error', f"Invalid date format: {e}"

# Example usage
expiration_date = "2024-12-25"
today = "2024-12-28"  # Optional; can be omitted to use the current date
status, message = check_item_availability(expiration_date, today)
print(f"Status: {status}, Message: {message}")

 
    else:
        sell_price = float(input('Voer de sell_price in '))

products.append({'id': id, 'product_name': product_name, 'bought_date': bought_date, 'bought_price': bought_price, 'expiration_date': expiration_date, 'sell_date': sell_date, 'sell_price': sell_price})
    
while True:
   doorgaan = input("Wil je nog een product toevoegen? (ja/nee): ").lower()
   if doorgaan != "ja":
      break

# CSV-file schrijven
with open('products', "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'product_name', 'bought_date', 'bought_price', 'expiration_date', 'sell_date', 'sell_price'])
    for product in products:
        writer.writerow([product['id'], product['product_name'], product['bought_date'], product['bought_price'], product['expiration_date'], product['sell_date'], product['sell_price']])

print(f"Productgegevens zijn opgeslagen in 'products' {products}")
'''
# Opbrengst en winst over bepaalde periode vaststellen
'''
import pandas as pd

csvfile = "products.csv"
data = pd.read_csv(csvfile)

data['bought_date'] = pd.to_datetime(data['bought_date'])
data['sell_date'] = pd.to_datetime(data['sell_date'])
data['expiration_date'] = pd.to_datetime(data['expiration_date'])

data['winst'] = data['sell_price'] - data['bought_price']

start_datum = input('Wat is de startdatum (YYYY-MM-DD) van de periode waarover u de opbrengst en winst wilt weten? ')
eind_datum = input('Wat is de einddatum (YYYY-MM-DD) van de periode waarover u de opbrengst en winst wilt weten? )')

gefilterde_data = data[(data['sell_date'] >= start_datum) & (data['sell_date'] <= eind_datum)]

totale_opbrengst = gefilterde_data['sell_price'].sum()
totale_winst = gefilterde_data['winst'].sum()

print(f"Totale opbrengst van {start_datum} tot {eind_datum}: €{totale_opbrengst}")
print(f"Totale winst van {start_datum} tot {eind_datum}: €{totale_winst}")

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    main()
