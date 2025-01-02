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
       if number == 1:
          print(f'Over 1 dag is het {date_after_number_days.strftime("%Y-%m-%d")}')
       else:
          print(f'Over {number} dagen is het {date_after_number_days.strftime("%Y-%m-%d")}')
       break
    else:
       print("Ongeldige invoer, probeer het opnieuw.")   
       
# products.csv 

# Invoer van productgegevens

krom datetime import datetime, date

products = []
today = date.today()  # Verkrijg de huidige datum

while True:
    # Invoer van productgegevens
    id = input('Voer de id in: ')
    product_name = input('Voer de product_name in: ')
    
    try:
        bought_date = datetime.strptime(input('Voer de bought_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
        expiration_date = datetime.strptime(input('Voer de expiration_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
        sell_date = datetime.strptime(input('Voer de sell_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
    except ValueError:
        print("Ongeldige datum ingevoerd. Probeer opnieuw.")
        continue

    try:
        bought_price = float(input('Voer de bought_price in: '))
    except ValueError:
        print("Ongeldige prijs ingevoerd. Probeer opnieuw.")
        continue

    # Controleer op verlopen product
    if today >= expiration_date:
        sell_price = 'expired'
        print('Het product is verlopen en niet meer beschikbaar voor verkoop.')
    else:
        print('Het product is nog beschikbaar voor verkoop.')
        try:
            sell_price = float(input('Voer de sell_price in: '))
        except ValueError:
            print("Ongeldige verkoopprijs ingevoerd. Probeer opnieuw.")
            continue

    # Product toevoegen aan de lijst
    products.append({
        'id': id,
        'product_name': product_name,
        'bought_date': bought_date,
        'bought_price': bought_price,
        'expiration_date': expiration_date,
        'sell_date': sell_date,
        'sell_price': sell_price
    })
    
    # Vraag of er meer producten toegevoegd moeten worden
    doorgaan = input("Wilt u nog een product toevoegen? (ja/nee): ").lower()
    if doorgaan != "ja":
        break

# Print de lijst van producten
print("\nToegevoegde producten:")
for product in products:
    print(product)

# CSV-file schrijven
with open('products.csv', "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'product_name', 'bought_date', 'bought_price', 'expiration_date', 'sell_date', 'sell_price'])
    for product in products:
        writer.writerow([product['id'], product['product_name'], product['bought_date'], product['bought_price'], product['expiration_date'], product['sell_date'], product['sell_price']])

print(f"Productgegevens zijn opgeslagen in 'products.csv' {products}")

# Opbrengst en winst over bepaalde periode vaststellen

import pandas as pd

# CSV-bestand inlezen
csvfile = "products.csv"
try:
    data = pd.read_csv(csvfile)
except FileNotFoundError:
    print(f"Het bestand '{csvfile}' kon niet worden gevonden.")
    exit()

# Datumkolommen omzetten naar datetime-formaat
try:
    data['bought_date'] = pd.to_datetime(data['bought_date'])
    data['sell_date'] = pd.to_datetime(data['sell_date'])
    data['expiration_date'] = pd.to_datetime(data['expiration_date'])
except KeyError as e:
    print(f"Verwachte kolom ontbreekt in het bestand: {e}")
    exit()

# Winst berekenen
try:
    data['winst'] = data['sell_price'] - data['bought_price']
except KeyError as e:
    print(f"Verwachte kolom ontbreekt in het bestand: {e}")
    exit()

# Periode opvragen van de gebruiker
while True:
    try:
        start_datum = pd.to_datetime(input('Wat is de startdatum (YYYY-MM-DD) van de periode waarover u de opbrengst en winst wilt weten? '))
        eind_datum = pd.to_datetime(input('Wat is de einddatum (YYYY-MM-DD) van de periode waarover u de opbrengst en winst wilt weten? '))
        if start_datum > eind_datum:
            print("De startdatum kan niet na de einddatum liggen. Probeer het opnieuw.")
            continue
        break
    except ValueError:
        print("Ongeldige invoer. Gebruik het formaat YYYY-MM-DD.")

# Data filteren binnen de opgegeven periode
gefilterde_data = data[(data['sell_date'] >= start_datum) & (data['sell_date'] <= eind_datum)]

# Opbrengst en winst berekenen
if not gefilterde_data.empty:
    totale_opbrengst = gefilterde_data['sell_price'].sum()
    totale_winst = gefilterde_data['winst'].sum()

    print(f"\nResultaten voor de periode van {start_datum.date()} tot {eind_datum.date()}:")
    print(f"Totale opbrengst: €{totale_opbrengst:.2f}")
    print(f"Totale winst: €{totale_winst:.2f}")
else:
    print(f"Geen verkopen gevonden tussen {start_datum.date()} en {eind_datum.date()}.")


import numpy as np
import matplotlib.pyplot as plt
'''
with open('data/small.txt', 'r') as f:
    data = np.genfromtxt(f, dtype='datetime64[s],f,f,f', 
                         names=['date', 'revenue', 'profit'])
datetime = data['date']
dayofyear = data['revenue']
temperature = data['profit']

import numpy as np
import matplotlib.pyplot as plt

# Adjust file path as necessary
file_path = 'data/small.txt'

# Ensure the data file structure matches the dtype
dtype = [('date', 'datetime64[s]'), ('revenue', 'f4'), ('profit', 'f4')]

# Read the file using genfromtxt
try:
    data = np.genfromtxt(file_path, delimiter=',', dtype=dtype, names=True)
    
    # Extract columns
    datetime = data['date']
    revenue = data['revenue']
    profit = data['profit']

    # Example plot (adjust according to your requirements)
    plt.figure(figsize=(10, 6))
    plt.plot(datetime, revenue, label='Revenue')
    plt.plot(datetime, profit, label='Profit')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Revenue and Profit Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

except FileNotFoundError:
    print(f"File {file_path} not found. Ensure the path is correct.")
except ValueError as e:
    print(f"Data format issue: {e}")
'''
import matplotlib.pyplot as plt

# Een grafiek van het verloop van opbrengst en winst over de gevraagde periode met maandelijkse meetpunten

data = {
    'Datum': pd.date_range(start=start_datum, end=eind_datum, freq='ME'),
    #'Opbrengst': [5000, 5200, 5100, 5300, 5500, 5700, 5900, 6000, 6200, 6100, 6300, 6400],
    #'Winst': [800, 850, 830, 900, 950, 1000, 1050, 1100, 1150, 1130, 1200, 1250]
}

# DataFrame maken
df = pd.DataFrame(data)

# Zet de datumkolom als index (optioneel, handig voor tijdreeksen)
#df.set_index('Datum', inplace=True)

# Plot de gegevens
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Opbrengst'], label='Opbrengst', marker='o')
plt.plot(df.index, df['Winst'], label='Winst', marker='s')

# Voeg labels en titel toe
plt.title('Opbrengst en Winst Over Tijd')
plt.xlabel('Datum')
plt.ylabel('Bedrag (€)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Toon de grafiek
plt.show()

if __name__ == "__main__":
    main()
