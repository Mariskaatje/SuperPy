import argparse
import csv
from datetime import datetime, timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
from rich import print
import os

__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Functie voor datumweergave
def show_today_date():
    today = date.today()
    datetime_to_string = today.strftime('%Y-%m-%d')
    print(f'Het is vandaag: {datetime_to_string}')

# Functie voor het verschuiven van de datum
def shift_today_date(days_forward=0):
    today = date.today()
    adjusted_today = today + timedelta(days=days_forward)
    print(f"De datum is opgeschoven naar: {adjusted_today.strftime('%Y-%m-%d')}")

# Functie om producten toe te voegen
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

    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'product_name', 'bought_date', 'bought_price', 'expiration_date', 'sell_date', 'sell_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(products)

    print(f"Alle producten zijn opgeslagen in {file_name}.")

# Functie om totale omzet en winst te berekenen
def calculate_total_revenue_and_profit(file_name, start_date, end_date):
    try:
        data = pd.read_csv(file_name, parse_dates=['bought_date', 'sell_date', 'expiration_date'])
        data['sell_price'] = pd.to_numeric(data['sell_price'], errors='coerce')
        data['bought_price'] = pd.to_numeric(data['bought_price'], errors='coerce')
        data = data.dropna(subset=['sell_price', 'bought_price', 'sell_date'])

        filtered_data = data[(data['sell_date'] >= start_date) & (data['sell_date'] <= end_date)]
        total_revenue = filtered_data['sell_price'].sum()
        total_profit = total_revenue - filtered_data['bought_price'].sum()
        return total_revenue, total_profit
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")
        return None, None

# Functie om maandelijkse gegevens te berekenen
def calculate_monthly_revenue_and_profit(file_name, start_date, end_date):
    try:
        # Lees het CSV-bestand en parseer datums
        df = pd.read_csv(file_name, parse_dates=['bought_date', 'sell_date', 'expiration_date'])
        
        # Controleer op verplichte kolommen
        required_columns = ['bought_date', 'sell_date', 'expiration_date', 'sell_price', 'bought_price']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Het bestand mist verplichte kolommen: {required_columns}")
        
        # Converteer waarden naar numeriek en drop lege rijen
        df['sell_price'] = pd.to_numeric(df['sell_price'], errors='coerce')
        df['bought_price'] = pd.to_numeric(df['bought_price'], errors='coerce')
        df = df.dropna(subset=['sell_price', 'bought_price'])

        # Filter verlopen producten uit
        today = pd.Timestamp.today()
        df = df[df['sell_price'] != 'expired']  # Verwijder expliciet als het gemarkeerd is als 'expired'
        df = df[df['sell_date'] <= df['expiration_date']]  # Verwijder als verkoopdatum na houdbaarheidsdatum is

        # Voeg een nieuwe kolom toe voor winst
        df['profit'] = df['sell_price'] - df['bought_price']
        
        # Filter de data op datumrange
        mask = (df['sell_date'] >= start_date) & (df['sell_date'] <= end_date)
        filtered_df = df[mask]

        if filtered_df.empty:
            print("Geen gegevens gevonden voor de opgegeven periode.")
            return None
        
        # Groepeer per maand
        filtered_df['month'] = filtered_df['sell_date'].dt.to_period('M')
        monthly_data = filtered_df.groupby('month').agg(
            revenue=('sell_price', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        
        # Converteer maand naar timestamp voor consistente weergave
        monthly_data['month'] = monthly_data['month'].dt.to_timestamp()
        return monthly_data

    except Exception as e:
        print(f"Fout bij berekening: {e}")
        return None

# Grafiek weergeven
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

# Main functie met argparse
def main():
    parser = argparse.ArgumentParser(description="Superpy voorraadbeheer.")
    parser.add_argument('--action', type=str, required=True, choices=['add', 'calculate', 'monthly', 'show_today', 'shift_date'], 
                        help='Kies een actie: add (producten toevoegen), calculate (totale omzet en winst berekenen), monthly (maandgegevens berekenen), show_today (datum weergeven), shift_date (datum vooruit schuiven), show_today (huidige datum tonen).')
    parser.add_argument('--start_date', type=str, help='Begindatum in het formaat YYYY-MM-DD.')
    parser.add_argument('--end_date', type=str, help='Einddatum in het formaat YYYY-MM-DD.')
    parser.add_argument('--number_of_days', type=int, help='Aantal dagen dat de datum vooruit geschoven moet.')
    parser.add_argument('--file_name', type=str, default='products.csv', help='De naam van het CSV-bestand.')
    
    args = parser.parse_args()

    if args.action == 'add':
        add_products_to_csv(args.file_name)

    elif args.action == 'calculate':
        if not (args.start_date and args.end_date):
            print("Voor de actie 'calculate' zijn --start_date en --end_date vereist.")
            return

        start_date = pd.to_datetime(args.start_date)
        end_date = pd.to_datetime(args.end_date)
        total_revenue, total_profit = calculate_total_revenue_and_profit(args.file_name, start_date, end_date)
        if total_revenue is not None and total_profit is not None:
            print(f"Totale omzet van {start_date.date()} tot {end_date.date()}: €{total_revenue:.2f}")
            print(f"Totale winst van {start_date.date()} tot {end_date.date()}: €{total_profit:.2f}")

    elif args.action == 'monthly':
        if not (args.start_date and args.end_date):
            print("Voor de actie 'monthly' zijn --start_date en --end_date vereist.")
            return

        start_date = pd.to_datetime(args.start_date)
        end_date = pd.to_datetime(args.end_date)
        monthly_data = calculate_monthly_revenue_and_profit(args.file_name, start_date, end_date)
        if monthly_data is not None and not monthly_data.empty:
            print("Maandelijkse omzet en winst:")
            print(monthly_data)
            plot_revenue_and_profit(monthly_data)

    elif args.action == 'show_today':
        today = date.today()
        show_today_date()
            
    elif args.action == 'shift_date':
        if args.number_of_days is None:
           print("Voor de actie 'shift_date' is --number_of_days vereist.")
           return
        today = date.today()
        shift_today_date(args. number_of_days)

if __name__ == '__main__': 
    main()
