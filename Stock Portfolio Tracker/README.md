# Stock Portfolio Tracker 📈

A comprehensive Python-based stock portfolio tracking application designed to calculate total investment value, monitor asset weights, manage custom stock prices, and export portfolio reports to TXT and CSV formats.

The project provides three user interfaces:
1. **Interactive CLI**: Command-line terminal interface.
2. **Desktop GUI**: Sleek Tkinter desktop interface with real-time portfolio management.
3. **Web Dashboard**: Interactive Streamlit web application with data visualization and charts.

---

## ✨ Features

- **Multi-Interface Support**: Run as a CLI tool, a desktop Tkinter GUI, or a modern Streamlit web dashboard.
- **Investment Calculation**: Automatically computes individual stock values, overall portfolio investment, and percentage weight allocations.
- **Custom Stock Prices**: Comes preloaded with standard stock prices (AAPL, TSLA, GOOGL, MSFT, etc.) while allowing dynamic user addition or updates.
- **Export Reports**: Save detailed portfolio summaries directly to `.csv` and `.txt` files.
- **Data Visualizations**: Visual allocation pie charts and breakdowns in the Streamlit app.
- **Automated Unit Tests**: Built-in test suite ensuring reliable mathematical calculations and data consistency.

---

## 📁 Project Structure

```
Stock Portfolio Tracker/
├── app_gui.py               # Tkinter desktop GUI application
├── app_streamlit.py         # Streamlit web dashboard application
├── portfolio_tracker.py     # Core logic and CLI application
├── test_portfolio_tracker.py# Unit tests
├── requirements.txt         # Project dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher installed on your system.

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd "Stock Portfolio Tracker"
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. Run the Streamlit Web Application
```bash
streamlit run app_streamlit.py
```

### 2. Run the Desktop GUI (Tkinter)
```bash
python app_gui.py
```

### 3. Run the Command-Line Interface (CLI)
```bash
python portfolio_tracker.py
```

### 4. Run Unit Tests
```bash
python -m unittest test_portfolio_tracker.py
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).

