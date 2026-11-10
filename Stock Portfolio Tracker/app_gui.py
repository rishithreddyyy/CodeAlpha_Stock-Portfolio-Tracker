"""
Stock Portfolio Tracker - Desktop GUI App (Tkinter)
--------------------------------------------------
A sleek desktop application built using Python's standard tkinter library.
Calculates total investment based on hardcoded stock prices and lets users 
add/remove stocks and export portfolio reports to TXT or CSV.
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Dict, List


# Default hardcoded stock prices
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


class PortfolioApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("900 x 650")
        self.root.minsize(800, 600)

        # Apply dark theme palette
        self.bg_color = "#1e1e2e"
        self.card_bg = "#252637"
        self.fg_color = "#cdd6f4"
        self.accent_blue = "#89b4fa"
        self.accent_green = "#a6e3a1"
        self.accent_red = "#f38ba8"
        self.entry_bg = "#313244"
        
        self.root.configure(bg=self.bg_color)
        
        # Portfolio Data Store: List of dicts
        self.portfolio: List[Dict] = []
        self.prices = STOCK_PRICES.copy()

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Treeview styling
        style.configure(
            "Treeview",
            background="#252637",
            foreground="#cdd6f4",
            fieldbackground="#252637",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        style.map("Treeview", background=[("selected", "#45475a")])
        style.configure(
            "Treeview.Heading",
            background="#313244",
            foreground="#89b4fa",
            font=("Segoe UI", 10, "bold")
        )

    def _build_ui(self):
        # Header Title Banner
        header_frame = tk.Frame(self.root, bg=self.card_bg, pady=15, padx=20)
        header_frame.pack(fill="x", side="top")

        title_lbl = tk.Label(
            header_frame, 
            text="📈 Stock Portfolio Tracker", 
            font=("Segoe UI", 20, "bold"), 
            fg=self.accent_blue, 
            bg=self.card_bg
        )
        title_lbl.pack(side="left")

        subtitle_lbl = tk.Label(
            header_frame, 
            text="Real-time total investment & asset allocation calculator", 
            font=("Segoe UI", 10, "italic"), 
            fg="#a6adc8", 
            bg=self.card_bg
        )
        subtitle_lbl.pack(side="left", padx=15, pady=5)

        # Main Layout: Left Control Panel + Right Portfolio Display
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        main_container.pack(fill="both", expand=True)

        # Left Panel (Inputs & Controls)
        left_panel = tk.LabelFrame(
            main_container, 
            text=" Add Stock Holding ", 
            font=("Segoe UI", 11, "bold"),
            fg=self.accent_blue, 
            bg=self.card_bg, 
            padx=15, 
            pady=15,
            bd=1,
            relief="solid"
        )
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        # Stock Selector Dropdown / Manual Entry
        tk.Label(left_panel, text="Stock Symbol:", font=("Segoe UI", 10), fg=self.fg_color, bg=self.card_bg).pack(anchor="w", pady=(5, 2))
        
        self.symbol_var = tk.StringVar()
        self.symbol_cb = ttk.Combobox(left_panel, textvariable=self.symbol_var, font=("Segoe UI", 10))
        self.symbol_cb['values'] = sorted(list(self.prices.keys()))
        self.symbol_cb.pack(fill="x", pady=(0, 10))
        self.symbol_cb.bind("<<ComboboxSelected>>", self._on_symbol_select)

        # Quantity Entry
        tk.Label(left_panel, text="Quantity (Shares):", font=("Segoe UI", 10), fg=self.fg_color, bg=self.card_bg).pack(anchor="w", pady=(5, 2))
        self.qty_var = tk.StringVar()
        self.qty_entry = tk.Entry(
            left_panel, 
            textvariable=self.qty_var, 
            font=("Segoe UI", 10),
            bg=self.entry_bg, 
            fg=self.fg_color, 
            insertbackground=self.fg_color
        )
        self.qty_entry.pack(fill="x", pady=(0, 10))

        # Stock Price Preview / Custom Price Entry
        tk.Label(left_panel, text="Price per Share ($):", font=("Segoe UI", 10), fg=self.fg_color, bg=self.card_bg).pack(anchor="w", pady=(5, 2))
        self.price_var = tk.StringVar()
        self.price_entry = tk.Entry(
            left_panel, 
            textvariable=self.price_var, 
            font=("Segoe UI", 10),
            bg=self.entry_bg, 
            fg=self.fg_color, 
            insertbackground=self.fg_color
        )
        self.price_entry.pack(fill="x", pady=(0, 15))

        # Action Buttons
        add_btn = tk.Button(
            left_panel, 
            text="➕ Add / Update Holding", 
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_green, 
            fg="#11111b", 
            activebackground="#89dceb",
            relief="flat", 
            command=self.add_holding,
            cursor="hand2",
            pady=6
        )
        add_btn.pack(fill="x", pady=(0, 8))

        del_btn = tk.Button(
            left_panel, 
            text="🗑️ Remove Selected", 
            font=("Segoe UI", 10),
            bg=self.accent_red, 
            fg="#11111b", 
            relief="flat", 
            command=self.remove_selected,
            cursor="hand2",
            pady=5
        )
        del_btn.pack(fill="x", pady=(0, 8))

        clear_btn = tk.Button(
            left_panel, 
            text="🔄 Clear All Holdings", 
            font=("Segoe UI", 10),
            bg="#45475a", 
            fg=self.fg_color, 
            relief="flat", 
            command=self.clear_all,
            cursor="hand2",
            pady=5
        )
        clear_btn.pack(fill="x", pady=(0, 15))

        # Quick Price Lookup Reference
        tk.Label(left_panel, text="Hardcoded Price Quick Ref:", font=("Segoe UI", 9, "bold"), fg="#a6adc8", bg=self.card_bg).pack(anchor="w", pady=(10, 2))
        
        self.ref_text = tk.Text(left_panel, height=8, width=24, bg=self.entry_bg, fg=self.fg_color, font=("Consolas", 9), relief="none")
        self.ref_text.pack(fill="both", expand=True)
        self._update_ref_text()

        # Right Panel (Portfolio Table & Summary Cards)
        right_panel = tk.Frame(main_container, bg=self.bg_color)
        right_panel.pack(side="right", fill="both", expand=True)

        # Summary Metric Card
        card_frame = tk.Frame(right_panel, bg=self.card_bg, padx=20, pady=15, bd=1, relief="solid")
        card_frame.pack(fill="x", pady=(0, 10))

        tk.Label(card_frame, text="TOTAL PORTFOLIO VALUE", font=("Segoe UI", 10, "bold"), fg="#a6adc8", bg=self.card_bg).pack(anchor="w")
        self.total_lbl = tk.Label(card_frame, text="$0.00", font=("Segoe UI", 24, "bold"), fg=self.accent_green, bg=self.card_bg)
        self.total_lbl.pack(anchor="w")

        # Table View
        table_frame = tk.Frame(right_panel, bg=self.bg_color)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("symbol", "price", "qty", "total", "weight")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("symbol", text="Stock Symbol")
        self.tree.heading("price", text="Price ($)")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("total", text="Total Value ($)")
        self.tree.heading("weight", text="Weight (%)")

        self.tree.column("symbol", width=110, anchor="center")
        self.tree.column("price", width=110, anchor="e")
        self.tree.column("qty", width=100, anchor="e")
        self.tree.column("total", width=140, anchor="e")
        self.tree.column("weight", width=100, anchor="e")

        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Export Buttons Bar
        export_bar = tk.Frame(right_panel, bg=self.bg_color)
        export_bar.pack(fill="x")

        save_txt_btn = tk.Button(
            export_bar, 
            text="📄 Export to TXT File", 
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_blue, 
            fg="#11111b", 
            relief="flat",
            command=self.export_txt,
            cursor="hand2",
            padx=15, 
            pady=6
        )
        save_txt_btn.pack(side="left", padx=(0, 10))

        save_csv_btn = tk.Button(
            export_bar, 
            text="📊 Export to CSV File", 
            font=("Segoe UI", 10, "bold"),
            bg="#b4befe", 
            fg="#11111b", 
            relief="flat",
            command=self.export_csv,
            cursor="hand2",
            padx=15, 
            pady=6
        )
        save_csv_btn.pack(side="left")

    def _update_ref_text(self):
        self.ref_text.config(state="normal")
        self.ref_text.delete("1.0", tk.END)
        for sym, pr in sorted(self.prices.items()):
            self.ref_text.insert(tk.END, f"{sym:<7} : ${pr:>8.2f}\n")
        self.ref_text.config(state="disabled")

    def _on_symbol_select(self, event=None):
        sym = self.symbol_var.get().strip().upper()
        if sym in self.prices:
            self.price_var.set(f"{self.prices[sym]:.2f}")

    def add_holding(self):
        sym = self.symbol_var.get().strip().upper()
        if not sym:
            messagebox.showwarning("Input Error", "Please enter or select a stock symbol.")
            return

        try:
            qty = float(self.qty_var.get().strip())
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive number for quantity.")
            return

        try:
            price = float(self.price_var.get().strip())
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive stock price.")
            return

        # Update dictionary price
        self.prices[sym] = price
        self.symbol_cb['values'] = sorted(list(self.prices.keys()))
        self._update_ref_text()

        # Update portfolio holding
        existing = next((item for item in self.portfolio if item["symbol"] == sym), None)
        if existing:
            existing["quantity"] += qty
            existing["price"] = price
            existing["total"] = existing["quantity"] * price
        else:
            self.portfolio.append({
                "symbol": sym,
                "price": price,
                "quantity": qty,
                "total": qty * price
            })

        self.refresh_table()
        self.qty_var.set("")

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please click a row in the table to remove.")
            return
        
        item_vals = self.tree.item(selected[0])["values"]
        sym = item_vals[0]
        self.portfolio = [item for item in self.portfolio if item["symbol"] != sym]
        self.refresh_table()

    def clear_all(self):
        if not self.portfolio:
            return
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to remove all portfolio holdings?"):
            self.portfolio.clear()
            self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_value = sum(item["total"] for item in self.portfolio)

        for item in self.portfolio:
            weight = (item["total"] / total_value * 100) if total_value > 0 else 0.0
            self.tree.insert("", "end", values=(
                item["symbol"],
                f"{item['price']:.2f}",
                f"{item['quantity']:.2f}",
                f"{item['total']:,.2f}",
                f"{weight:.1f}%"
            ))

        self.total_lbl.config(text=f"${total_value:,.2f}")

    def export_txt(self):
        if not self.portfolio:
            messagebox.showwarning("Empty Portfolio", "There are no holdings to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if not file_path:
            return

        total_value = sum(item["total"] for item in self.portfolio)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=====================================================\n")
            f.write("               STOCK PORTFOLIO TRACKER REPORT        \n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=====================================================\n\n")
            f.write(f"{'Symbol':<8} | {'Price ($)':>10} | {'Qty':>8} | {'Total Value ($)':>15} | {'Weight (%)':>10}\n")
            f.write("-" * 65 + "\n")
            for item in self.portfolio:
                weight = (item['total'] / total_value * 100) if total_value > 0 else 0.0
                f.write(f"{item['symbol']:<8} | ${item['price']:>9.2f} | {item['quantity']:>8.2f} | ${item['total']:>14.2f} | {weight:>9.1f}%\n")
            f.write("-" * 65 + "\n")
            f.write(f"TOTAL PORTFOLIO INVESTMENT VALUE: ${total_value:,.2f}\n")
            f.write("=====================================================\n")

        messagebox.showinfo("Export Successful", f"Saved portfolio report to:\n{file_path}")

    def export_csv(self):
        if not self.portfolio:
            messagebox.showwarning("Empty Portfolio", "There are no holdings to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        if not file_path:
            return

        total_value = sum(item["total"] for item in self.portfolio)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Price_USD", "Quantity", "Total_Value_USD", "Weight_Percent"])
            for item in self.portfolio:
                weight = (item['total'] / total_value * 100) if total_value > 0 else 0.0
                writer.writerow([
                    item["symbol"],
                    f"{item['price']:.2f}",
                    f"{item['quantity']:.2f}",
                    f"{item['total']:.2f}",
                    f"{weight:.1f}"
                ])
            writer.writerow([])
            writer.writerow(["TOTAL_INVESTMENT", "", "", f"{total_value:.2f}", "100.0"])

        messagebox.showinfo("Export Successful", f"Saved portfolio CSV to:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()
