"""
Stock Portfolio Tracker
-----------------------
A simple and intuitive tool to calculate total investment value based on 
manually defined stock prices and export results to TXT or CSV files.
"""

import csv
import os
from datetime import datetime
from typing import Dict, List, Tuple


# Hardcoded dictionary defining stock prices (in USD)
STOCK_PRICES: Dict[str, float] = {
    "AAPL": 180.50,
    "TSLA": 250.00,
    "GOOGL": 140.25,
    "AMZN": 175.80,
    "MSFT": 420.10,
    "NVDA": 120.40,
    "META": 500.60,
    "NFLX": 600.00,
    "AMD": 160.75,
    "INTC": 35.20,
}


def display_available_stocks(prices: Dict[str, float]) -> None:
    """Prints the list of available stocks and their current hardcoded prices."""
    print("\n" + "=" * 45)
    print("      AVAILABLE STOCK PRICES (HARDCODED)     ")
    print("=" * 45)
    print(f"{'Stock Symbol':<15} | {'Price ($)':>15}")
    print("-" * 45)
    for symbol, price in sorted(prices.items()):
        print(f"{symbol:<15} | ${price:>14.2f}")
    print("=" * 45 + "\n")


def add_custom_stock(prices: Dict[str, float]) -> None:
    """Allows user to add or update a stock price in the dictionary."""
    print("\n--- Add / Update Stock Price ---")
    symbol = input("Enter Stock Ticker Symbol (e.g. BTC, DIS): ").strip().upper()
    if not symbol:
        print("Invalid symbol. Returning to menu.")
        return

    while True:
        try:
            price_input = input(f"Enter price for {symbol} ($): ").strip()
            price = float(price_input)
            if price <= 0:
                print("Price must be greater than zero.")
                continue
            prices[symbol] = price
            print(f"✅ Successfully set {symbol} price to ${price:.2f}")
            break
        except ValueError:
            print("❌ Invalid input! Please enter a numeric price.")


def collect_user_portfolio(prices: Dict[str, float]) -> List[Dict[str, float]]:
    """
    Interactively prompts the user for stock symbols and quantities.
    Returns a list of dictionaries containing holding details.
    """
    portfolio: List[Dict[str, float]] = []
    print("\n" + "=" * 50)
    print("         BUILD YOUR STOCK PORTFOLIO           ")
    print("=" * 50)

    display_available_stocks(prices)

    while True:
        symbol = input("Enter Stock Symbol (or type 'DONE' to finish): ").strip().upper()
        
        if symbol == "DONE":
            break

        if not symbol:
            continue

        if symbol not in prices:
            print(f"⚠️ Stock '{symbol}' is not in the price list.")
            add_now = input(f"Would you like to add a price for {symbol}? (y/n): ").strip().lower()
            if add_now == 'y':
                try:
                    price = float(input(f"Enter price for {symbol} ($): ").strip())
                    if price > 0:
                        prices[symbol] = price
                        print(f"Added {symbol} at ${price:.2f}")
                    else:
                        print("Invalid price. Skipping stock.")
                        continue
                except ValueError:
                    print("Invalid numeric price. Skipping stock.")
                    continue
            else:
                print("Skipping stock.")
                continue

        # Get quantity
        while True:
            try:
                qty_str = input(f"Enter quantity of shares for {symbol}: ").strip()
                quantity = float(qty_str)
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
                break
            except ValueError:
                print("❌ Invalid input! Please enter a valid number for quantity.")

        price = prices[symbol]
        total_val = price * quantity

        # Check if already in portfolio
        existing = next((item for item in portfolio if item["symbol"] == symbol), None)
        if existing:
            existing["quantity"] += quantity
            existing["total"] = existing["quantity"] * existing["price"]
            print(f"Updated {symbol}: Total shares = {existing['quantity']}")
        else:
            portfolio.append({
                "symbol": symbol,
                "price": price,
                "quantity": quantity,
                "total": total_val
            })
            print(f"✅ Added {quantity} shares of {symbol} (${total_val:,.2f})")

        print("-" * 40)

    return portfolio


def calculate_portfolio_summary(portfolio: List[Dict[str, float]]) -> Tuple[float, List[Dict[str, float]]]:
    """Calculates total portfolio value and individual stock weightings."""
    total_investment = sum(item["total"] for item in portfolio)
    
    # Calculate percentage weight for each asset
    for item in portfolio:
        item["weight"] = (item["total"] / total_investment * 100) if total_investment > 0 else 0.0

    return total_investment, portfolio


def print_portfolio_summary(portfolio: List[Dict[str, float]], total_investment: float) -> None:
    """Prints a formatted summary of the portfolio."""
    if not portfolio:
        print("\nYour portfolio is currently empty!")
        return

    print("\n" + "=" * 65)
    print("                PORTFOLIO SUMMARY REPORT                 ")
    print("=" * 65)
    print(f"{'Symbol':<8} | {'Price ($)':>10} | {'Qty':>8} | {'Total Value ($)':>15} | {'Weight (%)':>10}")
    print("-" * 65)

    for item in portfolio:
        print(f"{item['symbol']:<8} | ${item['price']:>9.2f} | {item['quantity']:>8.2f} | ${item['total']:>14.2f} | {item['weight']:>9.1f}%")

    print("=" * 65)
    print(f"TOTAL INVESTMENT VALUE: ${total_investment:,.2f}")
    print("=" * 65 + "\n")


def save_portfolio_to_file(portfolio: List[Dict[str, float]], total_investment: float) -> None:
    """Prompts user to save portfolio details to a TXT or CSV file."""
    if not portfolio:
        print("Nothing to save. Portfolio is empty.")
        return

    print("\nSave Portfolio Options:")
    print("1. Save as Text File (.txt)")
    print("2. Save as CSV File (.csv)")
    print("3. Skip Saving")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "3" or choice == "":
        print("Skipped saving.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        filename = f"portfolio_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=====================================================\n")
            f.write("               STOCK PORTFOLIO TRACKER REPORT        \n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=====================================================\n\n")
            f.write(f"{'Symbol':<8} | {'Price ($)':>10} | {'Qty':>8} | {'Total Value ($)':>15} | {'Weight (%)':>10}\n")
            f.write("-" * 65 + "\n")
            for item in portfolio:
                f.write(f"{item['symbol']:<8} | ${item['price']:>9.2f} | {item['quantity']:>8.2f} | ${item['total']:>14.2f} | {item['weight']:>9.1f}%\n")
            f.write("-" * 65 + "\n")
            f.write(f"TOTAL PORTFOLIO INVESTMENT VALUE: ${total_investment:,.2f}\n")
            f.write("=====================================================\n")
        print(f"✅ Portfolio report saved successfully to '{filename}'!")

    elif choice == "2":
        filename = f"portfolio_{timestamp}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Price_USD", "Quantity", "Total_Value_USD", "Weight_Percent"])
            for item in portfolio:
                writer.writerow([
                    item["symbol"],
                    f"{item['price']:.2f}",
                    f"{item['quantity']:.2f}",
                    f"{item['total']:.2f}",
                    f"{item['weight']:.1f}"
                ])
            writer.writerow([])
            writer.writerow(["TOTAL_INVESTMENT", "", "", f"{total_investment:.2f}", "100.0"])
        print(f"✅ Portfolio data saved successfully to '{filename}'!")

    else:
        print("Invalid choice. Skipping save.")


def main():
    """Main application loop for CLI."""
    portfolio: List[Dict[str, float]] = []

    print("\n" + "*" * 55)
    print("    WELCOME TO THE STOCK PORTFOLIO TRACKER    ")
    print("*" * 55)

    while True:
        print("\nMAIN MENU:")
        print("1. View Available Stock Prices")
        print("2. Add / Update Stock Price in Price Dictionary")
        print("3. Enter / Add Stock Holdings")
        print("4. View Current Portfolio & Investment Total")
        print("5. Export / Save Portfolio to File (.txt / .csv)")
        print("6. Clear Portfolio")
        print("7. Exit Application")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            display_available_stocks(STOCK_PRICES)

        elif choice == "2":
            add_custom_stock(STOCK_PRICES)

        elif choice == "3":
            new_items = collect_user_portfolio(STOCK_PRICES)
            if new_items:
                # Merge into existing portfolio
                for new_item in new_items:
                    existing = next((x for x in portfolio if x["symbol"] == new_item["symbol"]), None)
                    if existing:
                        existing["quantity"] += new_item["quantity"]
                        existing["total"] = existing["quantity"] * existing["price"]
                    else:
                        portfolio.append(new_item)
                
                total_val, portfolio = calculate_portfolio_summary(portfolio)
                print_portfolio_summary(portfolio, total_val)

        elif choice == "4":
            total_val, portfolio = calculate_portfolio_summary(portfolio)
            print_portfolio_summary(portfolio, total_val)

        elif choice == "5":
            total_val, portfolio = calculate_portfolio_summary(portfolio)
            save_portfolio_to_file(portfolio, total_val)

        elif choice == "6":
            confirm = input("Are you sure you want to clear your current portfolio? (y/n): ").strip().lower()
            if confirm == 'y':
                portfolio.clear()
                print("Portfolio cleared.")

        elif choice == "7":
            print("\nThank you for using Stock Portfolio Tracker! Goodbye.\n")
            break

        else:
            print("❌ Invalid selection! Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()
