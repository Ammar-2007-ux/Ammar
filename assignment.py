import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt


# File to store transactions
DATA_FILE = "finance_data.csv"


# Initialize the main window
window = tk.Tk()
window.geometry("600x800")
window.title("Finance Tracker")


# Utility functions
def initialize_file():
    """Initialize the CSV file if it doesn't exist."""
    try:
        with open(DATA_FILE, "x") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Income", "Expense", "Category"])
    except FileExistsError:
        pass


def load_transactions():
    # Load transactions from the CSV file.
    transactions = []
    try:
        with open(DATA_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append({
                    "Date": row["Date"],
                    "Income": float(row["Income"]),
                    "Expense": float(row["Expense"]),
                    "Category": row["Category"]
                })
    except FileNotFoundError:
        initialize_file()
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")
    return transactions
def save_transaction(income, expense, category):
    # Save a transaction to the CSV file.
    try:
        with open(DATA_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), income, expense, category])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")
def sort_transactions(transactions, key):
    # Sort transactions by a given key
    return sorted(transactions, key=lambda x: x[key])
