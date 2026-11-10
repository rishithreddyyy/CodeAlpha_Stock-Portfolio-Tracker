"""
Stock Portfolio Tracker - Streamlit App
----------------------------------------
A simple web application to track stock holdings, calculate total investment
value, view portfolio allocation, and export summary reports.
"""

import io
import csv
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Default hardcoded stock prices (USD)
DEFAULT_STOCK_PRICES = {
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

# Configure Streamlit page layout
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="wide"
)

# Initialize session state for persistent data during re-runs
if "stock_prices" not in st.session_state:
    st.session_state.stock_prices = DEFAULT_STOCK_PRICES.copy()

if "portfolio" not in st.session_state:
    # Starting portfolio entries
    st.session_state.portfolio = [
        {"symbol": "AAPL", "quantity": 10.0},
        {"symbol": "TSLA", "quantity": 5.0},
        {"symbol": "NVDA", "quantity": 15.0},
        {"symbol": "MSFT", "quantity": 4.0},
    ]


# App Title & Overview
st.title("Stock Portfolio Tracker")
st.write("Track your stock investments, view percentage allocations, and download report summaries.")
st.divider()

# Sidebar - Adding Holdings & Price Customization
st.sidebar.header("Portfolio Inputs")

# Form to add a new stock holding
st.sidebar.subheader("Add / Update Holding")
available_symbols = sorted(list(st.session_state.stock_prices.keys()))
selected_stock = st.sidebar.selectbox("Select Stock:", available_symbols)
selected_qty = st.sidebar.number_input("Shares Quantity:", min_value=0.1, value=10.0, step=1.0)

if st.sidebar.button("Add to Portfolio", type="primary"):
    # Check if symbol already exists in portfolio
    found = False
    for item in st.session_state.portfolio:
        if item["symbol"] == selected_stock:
            item["quantity"] += selected_qty
            found = True
            break
    if not found:
        st.session_state.portfolio.append({"symbol": selected_stock, "quantity": selected_qty})
    st.sidebar.success(f"Added {selected_qty} shares of {selected_stock}")

st.sidebar.divider()

# Sidebar section to manage stock price list
with st.sidebar.expander("Manage Stock Prices"):
    st.write("Current Stock Price Reference:")
    price_table = pd.DataFrame(
        [{"Ticker": k, "Price ($)": v} for k, v in st.session_state.stock_prices.items()]
    )
    st.dataframe(price_table, use_container_width=True, hide_index=True)
    
    st.write("Add or Edit Ticker Price:")
    new_ticker = st.text_input("Ticker Symbol:").strip().upper()
    new_price = st.number_input("Price ($):", min_value=0.01, value=100.0, step=1.0)
    if st.button("Update Price"):
        if new_ticker:
            st.session_state.stock_prices[new_ticker] = new_price
            st.success(f"Set {new_ticker} to ${new_price:.2f}")
            st.rerun()

st.sidebar.divider()

if st.sidebar.button("Reset Portfolio"):
    st.session_state.portfolio = []
    st.rerun()


# Portfolio Calculation Logic
portfolio_rows = []
total_portfolio_value = 0.0

for holding in st.session_state.portfolio:
    symbol = holding["symbol"]
    qty = holding["quantity"]
    price = st.session_state.stock_prices.get(symbol, 0.0)
    total_val = qty * price
    total_portfolio_value += total_val
    portfolio_rows.append({
        "Symbol": symbol,
        "Price ($)": price,
        "Quantity": qty,
        "Total Value ($)": total_val
    })

df = pd.DataFrame(portfolio_rows)

if not df.empty and total_portfolio_value > 0:
    df["Weight (%)"] = (df["Total Value ($)"] / total_portfolio_value) * 100

# Top KPI Summary Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Portfolio Value", value=f"${total_portfolio_value:,.2f}")
with col2:
    st.metric(label="Total Positions", value=len(df))
with col3:
    if not df.empty:
        top_asset = df.loc[df["Total Value ($)"].idxmax()]["Symbol"]
        st.metric(label="Largest Asset Holding", value=top_asset)
    else:
        st.metric(label="Largest Asset Holding", value="N/A")

st.write("")

# Main Display Tabs
if not df.empty:
    tab_table, tab_chart = st.tabs(["Portfolio Holdings", "Asset Allocation Chart"])

    with tab_table:
        st.subheader("Holdings Summary")
        
        # Display formatted table
        formatted_df = df.copy()
        formatted_df["Price ($)"] = formatted_df["Price ($)"].apply(lambda x: f"${x:,.2f}")
        formatted_df["Quantity"] = formatted_df["Quantity"].apply(lambda x: f"{x:,.2f}")
        formatted_df["Total Value ($)"] = formatted_df["Total Value ($)"].apply(lambda x: f"${x:,.2f}")
        formatted_df["Weight (%)"] = formatted_df["Weight (%)"].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(formatted_df, use_container_width=True, hide_index=True)

        # Remove holding feature
        st.write("---")
        st.subheader("Remove Position")
        remove_symbol = st.selectbox("Select symbol to remove:", df["Symbol"].tolist())
        if st.button("Delete Position"):
            st.session_state.portfolio = [x for x in st.session_state.portfolio if x["symbol"] != remove_symbol]
            st.success(f"Removed {remove_symbol} from portfolio.")
            st.rerun()

    with tab_tab2 if 'tab_tab2' in locals() else tab_chart:
        st.subheader("Portfolio Distribution")
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.pie(
            df["Total Value ($)"],
            labels=df["Symbol"],
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.Paired.colors
        )
        ax.axis("equal")
        st.pyplot(fig)

    # Export Section
    st.write("---")
    st.subheader("Export Portfolio Data")
    
    col_exp1, col_exp2 = st.columns(2)

    # Create CSV string output
    csv_out = io.StringIO()
    writer = csv.writer(csv_out)
    writer.writerow(["Symbol", "Price_USD", "Quantity", "Total_Value_USD", "Weight_Percent"])
    for _, row in df.iterrows():
        writer.writerow([row["Symbol"], f"{row['Price ($)']:.2f}", f"{row['Quantity']:.2f}", f"{row['Total Value ($)']:.2f}", f"{row['Weight (%)']:.1f}"])
    writer.writerow([])
    writer.writerow(["TOTAL_PORTFOLIO_VALUE", "", "", f"{total_portfolio_value:.2f}", "100.0"])

    col_exp1.download_button(
        label="Download CSV Report",
        data=csv_out.getvalue(),
        file_name=f"portfolio_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # Create TXT string output
    txt_out = io.StringIO()
    txt_out.write("=====================================================\n")
    txt_out.write("               STOCK PORTFOLIO SUMMARY               \n")
    txt_out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    txt_out.write("=====================================================\n\n")
    txt_out.write(f"{'Symbol':<8} | {'Price ($)':>10} | {'Qty':>8} | {'Total Value ($)':>15} | {'Weight (%)':>10}\n")
    txt_out.write("-" * 65 + "\n")
    for _, row in df.iterrows():
        txt_out.write(f"{row['Symbol']:<8} | ${row['Price ($)']:>9.2f} | {row['Quantity']:>8.2f} | ${row['Total Value ($)']:>14.2f} | {row['Weight (%)']:>9.1f}%\n")
    txt_out.write("-" * 65 + "\n")
    txt_out.write(f"TOTAL PORTFOLIO VALUE: ${total_portfolio_value:,.2f}\n")
    txt_out.write("=====================================================\n")

    col_exp2.download_button(
        label="Download Text Summary (.txt)",
        data=txt_out.getvalue(),
        file_name=f"portfolio_summary_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

else:
    st.info("No stock holdings in portfolio. Add tickers from the sidebar to calculate total investment value.")
