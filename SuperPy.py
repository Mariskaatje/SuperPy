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
'''
# Vaststellen welke dag het is.

today = datetime.date.today()
print(f'Datum: {today}')

# Van datetime naar string  

datetime_to_string = today.strftime('%Y-%m-%d')

print(f'Het is vandaag {datetime_to_string}')

# Van string naar datetime

# string_to_datetime = datetime.datetime.strptime(today_string, '%Y_%m_%d')
# print(string_to_datetime)

from datetime import timedelta
today_date = datetime.date.today()

number = int(input('Hoeveel dagen wilt u de datum vooruit zetten?' ))
timedelta = datetime.timedelta(days=number)
date_after_number_days = today_date + timedelta
print(f'Over {number} dagen is het {date_after_number_days}')

# (python super.py --advance-time 2)
'''
# products.csv

with open('products.csv', 'w', newline='') as csvfile:
   fieldnames = ['ID','product_name','buy_date','buy_price','expiration_date', 'sell_date', 'sell_price']
   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)   

while True:
    ID = input('Voer een ID in ')
    if ID != '':
       print(f'Ingevoerde ID: {ID}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    product_name = input('Voer een product_name in ')
    if product_name != '':
       print(f'Ingevoerde product_name: {product_name}')
    else:
        print('Invoer mag niet leeg zijn.')
        break 

while True:
    buy_date = input('Voer een buy_date in ')
    if buy_date != '':
       print(f'Ingevoerde buy_date: {buy_date}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    buy_price = input('Voer een buy_price in ')
    if buy_price != '':
       print(f'Ingevoerde buy_price: {buy_price}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    expiration_date = input('Voer een expiration_date in ')
    if expiration_date != '':
       print(f'Ingevoerde expiration-date: {expiration_date}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    sell_date = input('Voer een sell_date in ')
    if sell_date != '':
       print(f'Ingevoerde sell_date: {sell_date}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   

while True:
    sell_price = input('Voer een sell_price in ')
    if sell_price != '':
       print(f'Ingevoerde sell_price: {sell_price}')
    else:
        print('Invoer mag niet leeg zijn.')
        break   
'''
# bought.csv

with open('bought.csv', 'w', newline='') as csvfile:
    fieldnames = ['ID','product_name','buy_date','buy_price','expiration_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
   
# sold.csv

with open('sold.csv', 'w', newline='') as csvfile:
    fieldnames = ['ID','sell_date','sell_price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

# bought.csv

with open ('bought.csv', 'r') as csvfile:
   reader = csv.DictReader('bought.csv')
   for row in reader:
      print(row['ID'], row['product_name'], row['buy_date'], row['buy_price'], row['expiration_date'])

for row in reader:
      if date >= expiration_date delete row

# sold.csv

with open ('sold.csv', 'r') as csvfile:   
   reader = csv.DictReader(csvfile)
   for row in reader:
      print(row['ID'], row['sell_date'], row['sell_price'])
'''
# products.csv      

with open('products.csv', newline='') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
      print(row['ID'], row['product_name'], row['buy_date'], ['buy_price'], ['expiration_date'], ['sell_date'], ['sell_price'])
'''             
#(Which products the supermarket offers;
#alle verschillende product_names van id s die niet verkocht of over datum zijn)

print('f De producten die de supermarkt aanbiedt zijn {[products]})

#(How many of each type of product the supermarket holds currently;
#het aantal id's van de aanwezige product_names)

print('f Per product is aanwezig {[product][aantal]})

#(How much each product was bought for, and what its expiry date is;
#de buy_price en expiration_date per id)

print(f'De aankoopprijs en huidbaarheidsdatum per product is{[ID][aankoopprijs][houdbaarheidsdatum]})

#(How much each product was sold for or if it expired, the fact that it did.
#de sell_price en of over datum per id)

print(f'De verkoopprijs en of over datum per product is{[ID][verkoopprijs][of over datum]})
'''
if __name__ == "__main__":
    main()

