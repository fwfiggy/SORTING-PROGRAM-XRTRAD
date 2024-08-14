import csv
import argparse
from collections import defaultdict

def load_team_map(filename):
    team_map = {}
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip header line
            for line in file:
                if line.strip():  # Check if the line is not empty
                    try:
                        team_id, team_name = line.strip().split(',', 1)
                        team_map[int(team_id)] = team_name
                    except ValueError:
                        print(f"Error parsing line: {line}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return team_map

def load_product_master(filename):
    product_master = {}
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip header line
            for line in file:
                if line.strip():  # Check if the line is not empty
                    try:
                        product_id, name, price, lot_size = line.strip().split(',')
                        product_master[int(product_id)] = {
                            'Name': name,
                            'Price': float(price),
                            'LotSize': int(lot_size)
                        }
                    except ValueError:
                        print(f"Error parsing line: {line}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return product_master

def load_sales(filename):
    sales = []
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip header line
            for line in file:
                if line.strip():  # Check if the line is not empty
                    try:
                        sale_id, product_id, team_id, quantity, discount = line.strip().split(',')
                        sales.append({
                            'SaleId': int(sale_id),
                            'ProductId': int(product_id),
                            'TeamId': int(team_id),
                            'Quantity': int(quantity),
                            'Discount': float(discount)
                        })
                    except ValueError:
                        print(f"Error parsing line: {line}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    return sales

def create_team_report(team_map, sales, product_master, team_report_file):
    team_sales = {}
    for sale in sales:
        team_id = sale['TeamId']  # Correct key name
        product_id = sale['ProductId']
        quantity = sale['Quantity']
        discount = sale['Discount']

        if team_id in team_map:
            product_info = product_master.get(product_id)
            if product_info:
                price = product_info['Price']
                lot_size = product_info['LotSize']
                revenue = price * quantity * lot_size
                gross_revenue = revenue / (1 - discount / 100.0)  # Calculate gross revenue

                if team_id in team_sales:
                    team_sales[team_id] += gross_revenue
                else:
                    team_sales[team_id] = gross_revenue

    sorted_team_sales = sorted(team_sales.items(), key=lambda x: x[1], reverse=True)

    with open(team_report_file, 'w') as file:
        file.write('Team,GrossRevenue\n')
        for team_id, revenue in sorted_team_sales:
            file.write(f'{team_map[team_id]},{revenue:.2f}\n')
            
def create_product_report(product_master, sales, product_report_file):
    product_sales = {}
    for sale in sales:
        product_id = sale['ProductId']  # Correct key name
        quantity = sale['Quantity']
        discount = sale['Discount']

        product_info = product_master.get(product_id)
        if product_info:
            price = product_info['Price']
            lot_size = product_info['LotSize']
            revenue = price * quantity * lot_size
            gross_revenue = revenue / (1 - discount / 100.0)  # Calculate gross revenue

            if product_id in product_sales:
                product_sales[product_id]['GrossRevenue'] += gross_revenue
                product_sales[product_id]['TotalUnits'] += quantity * lot_size
                product_sales[product_id]['DiscountCost'] += (price * quantity * lot_size) * (discount / 100.0)
            else:
                product_sales[product_id] = {
                    'Name': product_info['Name'],
                    'GrossRevenue': gross_revenue,
                    'TotalUnits': quantity * lot_size,
                    'DiscountCost': (price * quantity * lot_size) * (discount / 100.0)
                }

    sorted_product_sales = sorted(product_sales.values(), key=lambda x: x['GrossRevenue'], reverse=True)

    with open(product_report_file, 'w') as file:
        file.write('Name,GrossRevenue,TotalUnits,DiscountCost\n')
        for product_sale in sorted_product_sales:
            file.write(f"{product_sale['Name']},{product_sale['GrossRevenue']:.2f},{product_sale['TotalUnits']},{product_sale['DiscountCost']:.2f}\n")
def main():
    parser = argparse.ArgumentParser(description='Generate sales reports from input CSV files.')
    parser.add_argument('-t', '--team', required=True, help='Team map CSV file')
    parser.add_argument('-p', '--product', required=True, help='Product master CSV file')
    parser.add_argument('-s', '--sales', required=True, help='Sales CSV file')
    parser.add_argument('--team-report', required=True, help='Output team report CSV file')
    parser.add_argument('--product-report', required=True, help='Output product report CSV file')
    args = parser.parse_args()

    team_map = load_team_map(args.team)
    product_master = load_product_master(args.product)
    sales = load_sales(args.sales)

    create_team_report(team_map, sales, product_master, args.team_report)
    create_product_report(product_master, sales, args.product_report)

if __name__ == '__main__':
    main()