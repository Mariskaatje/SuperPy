# Imports
import argparse
import csv
from datetime import datetime, timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
from rich import print

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Functie om de datum vooruit te zetten
def adjust_date(current_date=None):
    if not current_date:
        current_date = datetime.now()
    while True:  
        datum_vooruit = input('Wilt u de datum vooruit zetten? (ja/nee) ').strip().lower()
        if datum_vooruit == 'nee':
            print(f'De datum blijft: {current_date.strftime("%Y-%m-%d")}')
            return current_date
        elif datum_vooruit == 'ja':
            try:
                number = int(input('Hoeveel dagen wilt u de datum vooruit zetten? '))
                new_date = current_date + timedelta(days=number)
                print(f'Nieuwe datum: {new_date.strftime("%Y-%m-%d")}')
                return new_date
            except ValueError:
                print('Ongeldige invoer. Voer een geldig getal in.')
        else:
            print('Ongeldige invoer. Probeer opnieuw.')

# Functie om producten toe te voegen aan CSV
def add_products_to_csv(file_name='products.csv'):
    products = []
    today = date.today()

    while True:
        try:
            id = input('Voer de id in: ')
            product_name = input('Voer de product_name in: ')
            bought_date = datetime.strptime(input('Voer de bought_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
            expiration_date = datetime.strptime(input('Voer de expiration_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
            sell_date = datetime.strptime(input('Voer de sell_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
            bought_price = float(input('Voer de bought_price in: '))
            sell_price = (
                'expired'
                if today >= expiration_date
                else float(input('Voer de sell_price in: '))
            )
        except ValueError as e:
            print(f'Fout: {e}. Probeer opnieuw.')
            continue

        products.append({
            'id': id,
            'product_name': product_name,
            'bought_date': bought_date,
            'bought_price': bought_price,
            'expiration_date': expiration_date,
            'sell_date': sell_date,
            'sell_price': sell_price
        })

        if input('Wilt u nog een product toevoegen? (ja/nee): ').strip().lower() != 'ja':
            break

    # Schrijf producten naar een CSV-bestand
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'product_name', 'bought_date', 'bought_price', 'expiration_date', 'sell_date', 'sell_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"Alle producten zijn opgeslagen in {file_name}.")

# Berekening van omzet en winst
def calculate_revenue_and_profit(csv_file, start_date, end_date):
    try:
        # Inlezen van CSV-bestand
        data = pd.read_csv(csv_file, parse_dates=['bought_date', 'sell_date', 'expiration_date'])
        
        # Zorg ervoor dat kolommen numeriek zijn
        data['sell_price'] = pd.to_numeric(data['sell_price'], errors='coerce')
        data['bought_price'] = pd.to_numeric(data['bought_price'], errors='coerce')
        
        # Verwijderen van rijen zonder noodzakelijke data
        data = data.dropna(subset=['sell_price', 'bought_price', 'sell_date'])
        
        # Filteren op de periode tussen start_date en end_date
        filtered_data = data[(data['sell_date'] >= start_date) & (data['sell_date'] <= end_date)]
        
        # Berekenen van omzet en winst
        revenue = filtered_data['sell_price'].sum()
        profit = revenue - filtered_data['bought_price'].sum()
        
        return revenue, profit
    except Exception as e:
        print(f"Fout bij het berekenen: {e}")
        return None, None

# Input voor start- en einddatum
try:
    start_date = pd.to_datetime(input("Voer de begindatum in (YYYY-MM-DD): "))
    end_date = pd.to_datetime(input("Voer de einddatum in (YYYY-MM-DD): "))
    
    # Controleer of start_date <= end_date
    if start_date > end_date:
        print("Fout: De begindatum kan niet later zijn dan de einddatum.")
    else:
        # Bereken omzet en winst
        revenue, profit = calculate_revenue_and_profit('products.csv', start_date, end_date)

        # Resultaten tonen
        if revenue is not None and profit is not None:
            print(f"Totaal omzet van {start_date.date()} tot {end_date.date()}: €{revenue:.2f}")
            print(f"Totaal winst van {start_date.date()} tot {end_date.date()}: €{profit:.2f}")
        else:
            print("Kon omzet en winst niet berekenen.")
except ValueError:
    print("Ongeldige datuminvoer. Zorg ervoor dat de datums in het formaat 'YYYY-MM-DD' zijn.")
   
# Berekening per maand
def calculate_monthly_revenue_and_profit(file_name, start_date, end_date):
    try:
        df = pd.read_csv(file_name, parse_dates=['bought_date', 'sell_date', 'expiration_date'])
        df['profit'] = df['sell_price'] - df['bought_price']
        mask = (df['sell_date'] >= start_date) & (df['sell_date'] <= end_date)
        filtered_df = df[mask]
        filtered_df['month'] = filtered_df['sell_date'].dt.to_period('M')
        monthly_data = filtered_df.groupby('month').agg(
            revenue=('sell_price', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        monthly_data['month'] = monthly_data['month'].dt.to_timestamp()
        return monthly_data
    except Exception as e:
        print(f"Fout bij berekening: {e}")
        return None

# Plotten van omzet en winst
def plot_revenue_and_profit(monthly_data):
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_data['month'], monthly_data['revenue'], label='Omzet', marker='o', linestyle='-')
    plt.plot(monthly_data['month'], monthly_data['profit'], label='Winst', marker='s', linestyle='--')
    plt.title('Omzet en Winst Over Tijd')
    plt.xlabel('Datum')
    plt.ylabel('Bedrag (in €)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

# Main-functie
def main():
    current_date = adjust_date()
    add_products_to_csv()
    start_date = pd.to_datetime(input('Voer de begindatum (YYYY-MM-DD) in: '))
    end_date = pd.to_datetime(input('Voer de einddatum (YYYY-MM-DD) in: '))
    monthly_data = calculate_monthly_revenue_and_profit('products.csv', start_date, end_date)
    if monthly_data is not None and not monthly_data.empty:
        print("Maandelijkse omzet en winst:")
        print(monthly_data)
        plot_revenue_and_profit(monthly_data)
    else:
        print("Geen gegevens beschikbaar voor de opgegeven periode.")

if __name__ == "__main__":
    main()
