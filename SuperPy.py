# Imports
import argparse
import csv
from datetime import datetime, timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
from rich import print
import os

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Functie om datum aan te passen
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

def add_products_to_csv(file_name='products.csv'):
    products = []
    today = date.today()

    while True:
        id = input('Voer de id in: ')
        product_name = input('Voer de product_name in: ')

        while True:
            try:
                bought_date = datetime.strptime(input('Voer de bought_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
                break
            except ValueError as e:
                print(f'Fout: {e}. Probeer opnieuw.')

        while True:
            try:
                expiration_date = datetime.strptime(input('Voer de expiration_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
                break
            except ValueError as e:
                print(f'Fout: {e}. Probeer opnieuw.')

        while True:
            try:
                sell_date = datetime.strptime(input('Voer de sell_date (YYYY-MM-DD) in: '), "%Y-%m-%d").date()
                break
            except ValueError as e:
                print(f'Fout: {e}. Probeer opnieuw.')

        while True:
            try:
                bought_price = float(input('Voer de bought_price in: '))
                break
            except ValueError as e:
                print(f'Fout: {e}. Probeer opnieuw.')

        if today > expiration_date:
            expired = input("Dit product is verlopen. Wilt u het als 'expired' markeren? (ja/nee): ").strip().lower()
            if expired == 'ja':
                sell_price = 'expired'
            else:
                while True:
                    try:
                        sell_price = float(input('Voer de sell_price in: '))
                        break
                    except ValueError as e:
                        print(f'Fout: {e}. Probeer opnieuw.')
        else:
            while True:
                try:
                    sell_price = float(input('Voer de sell_price in: '))
                    break
                except ValueError as e:
                    print(f'Fout: {e}. Probeer opnieuw.')

        # Voeg het product toe aan de lijst
        products.append({
            'id': id,
            'product_name': product_name,
            'bought_date': bought_date,
            'bought_price': bought_price,
            'expiration_date': expiration_date,
            'sell_date': sell_date,
            'sell_price': sell_price
        })

        # Vraag de gebruiker of er meer producten moeten worden toegevoegd
        if input('Wilt u nog een product toevoegen? (ja/nee): ').strip().lower() != 'ja':
            break

    # Schrijf producten naar CSV-bestand
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'product_name', 'bought_date', 'bought_price', 'expiration_date', 'sell_date', 'sell_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(products)

    print(f"Alle producten zijn opgeslagen in {file_name}.")

# Functie om totale omzet en winst over bepaalde peeriode te berekenen
def calculate_revenue_and_profit(csv_file, start_date, end_date):
    try:
        # Read CSV file
        data = pd.read_csv(csv_file, parse_dates=['bought_date', 'sell_date', 'expiration_date'])
        data = data.dropna(subset=['sell_price', 'bought_price', 'sell_date'])
        filtered_data = data[(data['sell_date'] >= start_date) & (data['sell_date'] <= end_date)]
        revenue = filtered_data['sell_price'].sum()
        profit = revenue - filtered_data['bought_price'].sum()
        return revenue, profit
    except Exception as e:
        print(f"Fout bij berekening: {e}")
        return None, None

# Functie om maandelijkse omzet en winst te berekenen
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

# Lijngrafiek van omzet en winst met maandelijkse meetpunten
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

# Main functie
def main():
    current_date = adjust_date()
    action = input("Wilt u producten toevoegen (1), maandgegevens berekenen (2) of totale omzet en winst berekenen (3)? ").strip()
    
    if action == "1":
        add_products_to_csv()
    elif action == "2":
        file_name = 'products.csv'
        if not os.path.exists(file_name):
            print(f"Het bestand '{file_name}' bestaat niet. Voeg eerst producten toe.")
            return

        start_date = pd.to_datetime(input('Voer de begindatum (YYYY-MM-DD) in van de periode waarover u de omzet en winst zien wilt '))
        end_date = pd.to_datetime(input('Voer de einddatum (YYYY-MM-DD) in van de periode waarover u de omzet en winst zien wilt '))
        monthly_data = calculate_monthly_revenue_and_profit(file_name, start_date, end_date)
        if monthly_data is not None and not monthly_data.empty:
            print("Maandelijkse omzet en winst:")
            print(monthly_data)
            plot_revenue_and_profit(monthly_data)
        else:
            print('Geen gegevens beschikbaar voor de opgegeven periode.')

    elif action == "3":
        # Bereken de totale omzet en winst voor de opgegeven periode
        file_name = 'products.csv'
        if not os.path.exists(file_name):
            print(f"Het bestand '{file_name}' bestaat niet. Voeg eerst producten toe.")
            return

        start_date = pd.to_datetime(input('Voer de begindatum (YYYY-MM-DD) in van de periode waarover u de omzet berekenen wilt '))
        end_date = pd.to_datetime(input('Voer de einddatum (YYYY-MM-DD) in van de periode waarover u de omzet en winst berekenen wilt '))
        
        total_revenue, total_profit = calculate_total_revenue_and_profit(file_name, start_date, end_date)
        if total_revenue is not None and total_profit is not None:
            print(f"Totale omzet van {start_date.date()} tot {end_date.date()}: €{total_revenue:.2f}")
            print(f"Totale winst van {start_date.date()} tot {end_date.date()}: €{total_profit:.2f}")
        else:
            print('Er was een probleem bij het berekenen van de totale omzet en winst.')

def calculate_total_revenue_and_profit(file_name, start_date, end_date):
   
    try:
        # CSV-bestand inlezen en data voorbereiden
        data = pd.read_csv(file_name, parse_dates=['bought_date', 'sell_date', 'expiration_date'])

        # Zorg ervoor dat kolommen numeriek zijn
        data['sell_price'] = pd.to_numeric(data['sell_price'], errors='coerce')
        data['bought_price'] = pd.to_numeric(data['bought_price'], errors='coerce')

        # Verwijder rijen zonder essentiële gegevens
        data = data.dropna(subset=['sell_price', 'bought_price', 'sell_date'])

        # Filter op periode
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = data[(data['sell_date'] >= start_date) & (data['sell_date'] <= end_date)]

        # Berekening van omzet en winst
        total_revenue = filtered_data['sell_price'].sum()
        total_profit = total_revenue - filtered_data['bought_price'].sum()

        return total_revenue, total_profit

    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
        return None, None

if __name__ == '__main__':
    main()
