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

# Vaststellen welke dag het is

today = datetime.date.today()
print(today)

# Van datetime naar string  

datetime_to_string = today.strftime('%Y-%m-%d')

print(datetime_to_string)

# Van string naar datetime

#string_to_datetime = datetime.datetime.strptime(today_string, '%Y_%m_%d')
#print(string_to_datetime)

from datetime import timedelta
today_date = datetime.date.today()
timedelta = datetime.timedelta(days=2)
print(today_date)
date_after_2_days = today_date + timedelta
print(date_after_2_days)

#(python super.py --advance-time 2)

# bought.csv

while True:
    id_input = input('Voer een id in ')
    if id_input != '':
       print(f'Ingevoerde id: (id_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    product_name_input = input('Voer een product_name in ')
    if product_name_input != '':
       print(f'Ingevoerde product_name: (product_name_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break 

while True:
    buy_date_input = input('Voer een buy_date in ')
    if buy_date_input != '':
       print(f'Ingevoerde buy_date: (buy_date_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    buy_price_input = input('Voer een buy_price in ')
    if buy_price_input != '':
       print(f'Ingevoerde buy_price: (buy_price_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    expiration_date_input = input('Voer een expiration_date in ')
    if expiration_date_input != '':
       print(f'Ingevoerde expiration-date: (expiration_date_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    bought_id_input = input('Voer een bought_id in ')
    if bought_id_input != '':
       print(f'Ingevoerde bought_id: (bought_id_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    sell_date_input = input('Voer een sell_date in ')
    if sell_date_input != '':
       print(f'Ingevoerde sell_date: (sell_date_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    sell_price_input = input('Voer een sell_price in ')
    if sell_price_input != '':
       print(f'Ingevoerde sell_price: (sell_price_input)')
    else:
        print('Invoer mag niet leeg zijn.')
        break   
'''
#bought.csv

with open('bought.csv', 'w', newline='') as csvfile:
    fieldnames = ['id_input','product_name','buy_date','buy_price','expiration_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
   
#sold.csv

with open('sold.csv', 'w', newline='') as csvfile:
    fieldnames = ['id','bought_id','sell_date','sell_price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
'''
#bought.csv

with open ('bought.csv', 'r') as csvfile:
   reader = csv.DictReader('bought.csv')
   for row in reader:
      print(row['id'], row['product_name'], row['buy_date'], row['buy_price'], row['expiration_date'])

#sold.csv

with open ('sold.csv', 'r') as csvfile:   
   reader = csv.DictReader(csvfile)
   for row in reader:
    print(row['id'], row['bought_id'], row['sell_date'], row['sell_price'])
'''
#(Which products the supermarket offers;
alle verschillende product_names van id s die niet verkocht of over datum zijn)

#(How many of each type of product the supermarket holds currently;
het aantal id's van de aanwezige product_names)

#(How much each product was bought for, and what its expiry date is;
de buy_price en expiration_date per id)

#(How much each product was sold for or if it expired, the fact that it did.
de sell_price en of over datum per id)
'''
if __name__ == "__main__":
    main()
