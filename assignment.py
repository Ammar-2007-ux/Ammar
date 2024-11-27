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
def search_transactions(transactions, category):
    # Search transactions by category
    return [t for t in transactions if t["Category"].lower() == category.lower()]
def add_transaction():
    # Add a new transaction.
    income = income_entry.get()
    expense = expense_entry.get()
    category = category_dropdown.get()

    if not (income or expense) or category == "Select Category":
        messagebox.showerror("Error", "Please fill all fields!")
        return

    try:
        income = float(income) if income else 0.0
        expense = float(expense) if expense else 0.0
        save_transaction(income, expense, category)
        income_entry.delete(0, tk.END)
        expense_entry.delete(0, tk.END)
        category_dropdown.set("Select Category")
        display_transactions()
        messagebox.showinfo("Success", "Transaction added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Income and Expense must be numeric values!")

def display_transactions():
    # Display all transactions in the text area
    transactions = load_transactions()
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"{'Date':<20}{'Income':<10}{'Expense':<10}{'Category'}\n")
    text_area.insert(tk.END, "-" * 50 + "\n")
    for t in transactions:
        text_area.insert(
            tk.END, f"{t['Date']:<20}{t['Income']:<10}{t['Expense']:<10}{t['Category']}\n"
        )
