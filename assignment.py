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


