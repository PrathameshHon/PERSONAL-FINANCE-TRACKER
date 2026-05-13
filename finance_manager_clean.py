import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pickle
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ======================== DATA STORAGE ========================
monthly_income = {}      # Stores income sources for each month
monthly_budget = {}      # Stores budget categories for each month
expense_records = []     # Stores all expenses (month, date, category, amount)
account_balance = {}     # Tracks balance for each month

# ======================== FILE OPERATIONS ========================
def save_data():
    """Save all financial data to a file for persistence."""
    data = {
        "monthly_income": monthly_income,
        "monthly_budget": monthly_budget,
        "expense_records": expense_records,
        "account_balance": account_balance
    }
    try:
        with open("finance_data.pkl", "wb") as file:
            pickle.dump(data, file)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data: {e}")

def load_data():
    """Load financial data from file when program starts."""
    global monthly_income, monthly_budget, expense_records, account_balance
    try:
        if os.path.exists("finance_data.pkl"):
            with open("finance_data.pkl", "rb") as file:
                data = pickle.load(file)
                monthly_income = data.get("monthly_income", {})
                monthly_budget = data.get("monthly_budget", {})
                expense_records = data.get("expense_records", [])
                account_balance = data.get("account_balance", {})
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load data: {e}")

# ======================== INCOME MANAGEMENT ========================
def add_income_gui():
    """Open window to add monthly income sources."""
    income_window = tk.Toplevel(root)
    income_window.title("Add Monthly Income")
    income_window.geometry("400x300")

    # Month input
    tk.Label(income_window, text="Enter Month (01-12):", font=("Arial", 10)).pack(pady=5)
    month_entry = tk.Entry(income_window, width=20)
    month_entry.pack()

    # Dynamic income sources
    income_sources = []

    def add_income_source():
        frame = tk.Frame(income_window)
        frame.pack(pady=5)

        tk.Label(frame, text="Source Name:").pack(side=tk.LEFT, padx=5)
        source_name = tk.Entry(frame, width=15)
        source_name.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        source_amount = tk.Entry(frame, width=10)
        source_amount.pack(side=tk.LEFT, padx=5)

        income_sources.append((source_name, source_amount))

    def submit_income():
        month = month_entry.get().strip()

        # Validation
        if not month:
            messagebox.showerror("Error", "Please enter a month")
            return
        
        if not month.isdigit() or not (1 <= int(month) <= 12):
            messagebox.showerror("Error", "Month must be 01-12")
            return

        income_dict = {}
        total_income = 0

        for source_name_widget, source_amount_widget in income_sources:
            source_name = source_name_widget.get().strip()
            source_amount_str = source_amount_widget.get().strip()

            if source_name and source_amount_str:
                try:
                    amount = int(source_amount_str)
                    if amount < 0:
                        messagebox.showerror("Error", "Amount cannot be negative")
                        return
                    income_dict[source_name] = amount
                    total_income += amount
                except ValueError:
                    messagebox.showerror("Error", "Enter valid numbers for amounts")
                    return

        if not income_dict:
            messagebox.showerror("Error", "Add at least one income source")
            return

        monthly_income[month] = income_dict
        account_balance[month] = total_income

        save_data()
        messagebox.showinfo("Success", f"Income Added!\nTotal: ₹{total_income}")
        income_window.destroy()

    tk.Button(income_window, text="Add Source", command=add_income_source, bg="lightblue").pack(pady=5)
    tk.Button(income_window, text="Submit", command=submit_income, bg="lightgreen").pack(pady=5)

# ======================== BUDGET MANAGEMENT ========================
def add_budget_gui():
    """Open window to add monthly budget categories."""
    budget_window = tk.Toplevel(root)
    budget_window.title("Add Monthly Budget")
    budget_window.geometry("400x300")

    # Month input
    tk.Label(budget_window, text="Enter Month (01-12):", font=("Arial", 10)).pack(pady=5)
    month_entry = tk.Entry(budget_window, width=20)
    month_entry.pack()

    # Dynamic budget categories
    budget_categories = []

    def add_budget_category():
        frame = tk.Frame(budget_window)
        frame.pack(pady=5)

        tk.Label(frame, text="Category:").pack(side=tk.LEFT, padx=5)
        category_name = tk.Entry(frame, width=15)
        category_name.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        category_amount = tk.Entry(frame, width=10)
        category_amount.pack(side=tk.LEFT, padx=5)

        budget_categories.append((category_name, category_amount))

    def submit_budget():
        month = month_entry.get().strip()

        # Validation
        if not month:
            messagebox.showerror("Error", "Please enter a month")
            return
        
        if not month.isdigit() or not (1 <= int(month) <= 12):
            messagebox.showerror("Error", "Month must be 01-12")
            return

        budget_dict = {}

        for category_widget, amount_widget in budget_categories:
            category = category_widget.get().strip()
            amount_str = amount_widget.get().strip()

            if category and amount_str:
                try:
                    amount = int(amount_str)
                    if amount < 0:
                        messagebox.showerror("Error", "Amount cannot be negative")
                        return
                    budget_dict[category] = amount
                except ValueError:
                    messagebox.showerror("Error", "Enter valid numbers for amounts")
                    return

        if not budget_dict:
            messagebox.showerror("Error", "Add at least one budget category")
            return

        monthly_budget[month] = budget_dict

        save_data()
        messagebox.showinfo("Success", "Budget Added Successfully!")
        budget_window.destroy()

    tk.Button(budget_window, text="Add Category", command=add_budget_category, bg="lightblue").pack(pady=5)
    tk.Button(budget_window, text="Submit", command=submit_budget, bg="lightgreen").pack(pady=5)

# ======================== EXPENSE MANAGEMENT ========================
def add_expense_gui():
    """Open window to add individual expenses."""
    expense_window = tk.Toplevel(root)
    expense_window.title("Add Expense")
    expense_window.geometry("400x350")

    tk.Label(expense_window, text="Enter Month (01-12):", font=("Arial", 10)).pack(pady=5)
    month_entry = tk.Entry(expense_window, width=20)
    month_entry.pack()

    tk.Label(expense_window, text="Enter Date (DD-MM-YYYY):", font=("Arial", 10)).pack(pady=5)
    date_entry = tk.Entry(expense_window, width=20)
    date_entry.pack()

    tk.Label(expense_window, text="Category:", font=("Arial", 10)).pack(pady=5)
    category_entry = tk.Entry(expense_window, width=20)
    category_entry.pack()

    tk.Label(expense_window, text="Amount (₹):", font=("Arial", 10)).pack(pady=5)
    amount_entry = tk.Entry(expense_window, width=20)
    amount_entry.pack()

    def submit_expense():
        month = month_entry.get().strip()
        date = date_entry.get().strip()
        category = category_entry.get().strip()
        amount_str = amount_entry.get().strip()

        # Validation
        if not month or not date or not category or not amount_str:
            messagebox.showerror("Error", "Please fill all fields")
            return

        if not month.isdigit() or not (1 <= int(month) <= 12):
            messagebox.showerror("Error", "Month must be 01-12")
            return

        # Validate date format
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Date format must be DD-MM-YYYY")
            return

        try:
            amount = int(amount_str)
            if amount < 0:
                messagebox.showerror("Error", "Amount cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number")
            return

        # Add expense record
        expense_records.append((month, date, category, amount))
        account_balance[month] = account_balance.get(month, 0) - amount

        save_data()

        remaining = account_balance[month]
        messagebox.showinfo("Success", f"Expense Added!\nRemaining Balance: ₹{remaining}")
        expense_window.destroy()

    tk.Button(expense_window, text="Submit", command=submit_expense, bg="lightgreen").pack(pady=5)

# ======================== VISUALIZATIONS ========================
def show_pie_chart():
    """Display pie chart of expense distribution by category."""
    if not expense_records:
        messagebox.showerror("Error", "No expense data available!")
        return

    try:
        df = pd.DataFrame(expense_records, columns=["Month", "Date", "Category", "Amount"])
        category_totals = df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(8, 6))
        plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
        plt.title("Expense Distribution by Category", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Chart Error", f"Could not generate chart: {e}")

# ======================== REPORT GENERATION ========================
def create_report():
    """Generate Excel report with expense details and monthly summary."""
    try:
        # Create expense dataframe
        if expense_records:
            df_expenses = pd.DataFrame(expense_records, columns=["Month", "Date", "Category", "Amount"])
        else:
            df_expenses = pd.DataFrame(columns=["Month", "Date", "Category", "Amount"])

        # Create summary dataframe
        summary_list = []

        for month in monthly_income.keys():
            total_income = sum(monthly_income.get(month, {}).values())
            total_budget = sum(monthly_budget.get(month, {}).values())
            total_expense = df_expenses[df_expenses["Month"] == month]["Amount"].sum()
            
            if pd.isna(total_expense):
                total_expense = 0

            net_saving = total_income - total_expense

            summary_list.append({
                "Month": month,
                "Total Income": total_income,
                "Total Budget": total_budget,
                "Total Expense": int(total_expense),
                "Saving/Loss": int(net_saving)
            })

        df_summary = pd.DataFrame(summary_list)

        # Save to Desktop
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        file_path = os.path.join(desktop_path, "Finance_Report.xlsx")

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df_expenses.to_excel(writer, sheet_name="Expense Details", index=False)
            df_summary.to_excel(writer, sheet_name="Monthly Summary", index=False)

        # Open the file
        os.startfile(file_path)
        messagebox.showinfo("Success", f"Report Generated!\n\nSaved to: {file_path}")

    except Exception as e:
        messagebox.showerror("Report Error", f"Could not generate report: {e}")

# ======================== MAIN WINDOW ========================
root = tk.Tk()
root.title("Personal Finance Manager")
root.geometry("450x500")
root.config(bg="#f0f0f0")

# Header
header = tk.Label(root, text="💰 Personal Finance Manager 💰", 
                   font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10)
header.pack(fill=tk.X)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

buttons_config = [
    ("📊 Add Income", add_income_gui),
    ("💼 Add Budget", add_budget_gui),
    ("💸 Add Expense", add_expense_gui),
    ("📈 Generate Report", create_report),
    ("🥧 Show Pie Chart", show_pie_chart)
]

for text, command in buttons_config:
    btn = tk.Button(button_frame, text=text, width=30, height=2, 
                    command=command, font=("Arial", 10), bg="#2196F3", fg="white",
                    activebackground="#0b7dda", cursor="hand2")
    btn.pack(pady=8)

# Footer
footer = tk.Label(root, text="All data is saved automatically", 
                  font=("Arial", 9, "italic"), bg="#f0f0f0", fg="gray")
footer.pack(side=tk.BOTTOM, pady=10)

# Load existing data
load_data()

# Run application
root.mainloop()
