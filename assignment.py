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
def sort_and_display(key):
    # Sort transactions and display them.
    transactions = load_transactions()
    sorted_transactions = sort_transactions(transactions, key)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"{'Date':<20}{'Income':<10}{'Expense':<10}{'Category'}\n")
    text_area.insert(tk.END, "-" * 50 + "\n")
    for t in sorted_transactions:
        text_area.insert(
            tk.END, f"{t['Date']:<20}{t['Income']:<10}{t['Expense']:<10}{t['Category']}\n"
        )
        def search_and_display():
    # Search transactions by category and display results.
    category = search_entry.get()
    if not category:
        messagebox.showerror("Error", "Please enter a category to search!")
        return
    transactions = load_transactions()
    results = search_transactions(transactions, category)
    if not results:
        messagebox.showinfo("No Results", f"No transactions found for category '{category}'.")
    else:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"{'Date':<20}{'Income':<10}{'Expense':<10}{'Category'}\n")
        text_area.insert(tk.END, "-" * 50 + "\n")
        for t in results:
            text_area.insert(
                tk.END, f"{t['Date']:<20}{t['Income']:<10}{t['Expense']:<10}{t['Category']}\n"
            )
            def visualize_expenses():
    # Visualize expenses by category using a pie chart.
    transactions = load_transactions()
    categories = {}
    for t in transactions:
        if t["Category"] in categories:
            categories[t["Category"]] += t["Expense"]
        else:
            categories[t["Category"]] = t["Expense"]
 if categories:
        plt.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%")
        plt.title("Expense Distribution")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses to visualize.")


# GUI Layout
# Title
label = tk.Label(window, text="Finance Tracker", font=("Bold", 18))
label.pack(pady=20)

# Input Frame
input_frame = ttk.Frame(window)
input_frame.pack(pady=10)
tk.Label(input_frame, text="Income:").grid(row=0, column=0, padx=10, pady=5)
income_entry = ttk.Entry(input_frame)
income_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Expense:").grid(row=1, column=0, padx=10, pady=5)
expense_entry = ttk.Entry(input_frame)
expense_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=10, pady=5)
categories = ["Food", "Rent", "Utilities", "Entertainment", "Other"]
category_dropdown = ttk.Combobox(input_frame, values=categories)
category_dropdown.grid(row=2, column=1)
category_dropdown.set("Select Category")

add_button = tk.Button(window, text="Add Transaction", command=add_transaction)
add_button.pack(pady=10)
# Transaction Display
text_area = tk.Text(window, font=("Arial", 12), height=10, width=70)
text_area.pack(pady=10)

# Sorting and Searching
sort_frame = ttk.Frame(window)
sort_frame.pack(pady=10)
tk.Label(sort_frame, text="Sort by:").grid(row=0, column=0, padx=10)
sort_income_button = tk.Button(sort_frame, text="Income", command=lambda: sort_and_display("Income"))
sort_income_button.grid(row=0, column=1, padx=5)
sort_expense_button = tk.Button(sort_frame, text="Expense", command=lambda: sort_and_display("Expense"))
sort_expense_button.grid(row=0, column=2, padx=5)
sort_date_button = tk.Button(sort_frame, text="Date", command=lambda: sort_and_display("Date"))
sort_date_button.grid(row=0, column=3, padx=5)
tk.Label(sort_frame, text="Search by Category:").grid(row=1, column=0, padx=10, pady=10)
search_entry = ttk.Entry(sort_frame)
search_entry.grid(row=1, column=1)
search_button = tk.Button(sort_frame, text="Search", command=search_and_display)
search_button.grid(row=1, column=2, padx=5)
# Visualization Button
visualize_button = tk.Button(window, text="Visualize Expenses", command=visualize_expenses)
visualize_button.pack(pady=10)