import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ======================== CONFIG ========================
st.set_page_config(page_title="Personal Finance Manager", page_icon="💰", layout="centered")
DATA_FILE = "finance_data.json"

# ======================== DATA STORAGE ========================
def load_data():
    """Load financial data from file, or initialize empty structures."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return (
                    data.get("monthly_income", {}),
                    data.get("monthly_budget", {}),
                    data.get("expense_records", []),
                    data.get("account_balance", {}),
                )
        except Exception as e:
            st.error(f"Could not load data: {e}")
    return {}, {}, [], {}

def save_data():
    """Save all financial data to a file for persistence."""
    data = {
        "monthly_income": st.session_state.monthly_income,
        "monthly_budget": st.session_state.monthly_budget,
        "expense_records": st.session_state.expense_records,
        "account_balance": st.session_state.account_balance,
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Could not save data: {e}")

# Initialize session state once
if "monthly_income" not in st.session_state:
    (
        st.session_state.monthly_income,
        st.session_state.monthly_budget,
        st.session_state.expense_records,
        st.session_state.account_balance,
    ) = load_data()

if "income_rows" not in st.session_state:
    st.session_state.income_rows = 1
if "budget_rows" not in st.session_state:
    st.session_state.budget_rows = 1

# ======================== HEADER ========================
st.markdown(
    "<h1 style='text-align:center; color:white; background-color:#4CAF50; "
    "padding:12px; border-radius:8px;'>💰 Personal Finance Manager 💰</h1>",
    unsafe_allow_html=True,
)
st.write("")

tabs = st.tabs(["📊 Income", "💼 Budget", "💸 Expense", "🥧 Chart", "📈 Report"])

# ======================== INCOME TAB ========================
with tabs[0]:
    st.subheader("Add Monthly Income")
    month = st.text_input("Month (01-12)", key="income_month")

    st.write("Income Sources")
    if st.button("+ Add Source"):
        st.session_state.income_rows += 1

    sources = []
    for i in range(st.session_state.income_rows):
        c1, c2 = st.columns(2)
        name = c1.text_input(f"Source name {i+1}", key=f"inc_name_{i}")
        amount = c2.number_input(f"Amount {i+1}", min_value=0, step=100, key=f"inc_amt_{i}")
        sources.append((name, amount))

    if st.button("Submit Income", type="primary"):
        if not month or not month.isdigit() or not (1 <= int(month) <= 12):
            st.error("Month must be 01-12")
        else:
            month_key = month.zfill(2)
            income_dict = {name: amt for name, amt in sources if name and amt > 0}
            if not income_dict:
                st.error("Add at least one income source")
            else:
                total_income = sum(income_dict.values())
                st.session_state.monthly_income[month_key] = income_dict
                st.session_state.account_balance[month_key] = total_income
                save_data()
                st.success(f"Income Added! Total: ₹{total_income}")

# ======================== BUDGET TAB ========================
with tabs[1]:
    st.subheader("Add Monthly Budget")
    b_month = st.text_input("Month (01-12)", key="budget_month")

    st.write("Budget Categories")
    if st.button("+ Add Category"):
        st.session_state.budget_rows += 1

    categories = []
    for i in range(st.session_state.budget_rows):
        c1, c2 = st.columns(2)
        cat = c1.text_input(f"Category {i+1}", key=f"bud_cat_{i}")
        amt = c2.number_input(f"Amount {i+1}", min_value=0, step=100, key=f"bud_amt_{i}")
        categories.append((cat, amt))

    if st.button("Submit Budget", type="primary"):
        if not b_month or not b_month.isdigit() or not (1 <= int(b_month) <= 12):
            st.error("Month must be 01-12")
        else:
            month_key = b_month.zfill(2)
            budget_dict = {cat: amt for cat, amt in categories if cat and amt > 0}
            if not budget_dict:
                st.error("Add at least one budget category")
            else:
                st.session_state.monthly_budget[month_key] = budget_dict
                save_data()
                st.success("Budget Added Successfully!")

# ======================== EXPENSE TAB ========================
with tabs[2]:
    st.subheader("Add Expense")
    e_month = st.text_input("Month (01-12)", key="exp_month")
    e_date = st.text_input("Date (DD-MM-YYYY)", key="exp_date")
    e_category = st.text_input("Category", key="exp_category")
    e_amount = st.number_input("Amount (₹)", min_value=0, step=50, key="exp_amount")

    if st.button("Add Expense", type="primary"):
        if not e_month or not e_date or not e_category or e_amount <= 0:
            st.error("Please fill all fields")
        elif not e_month.isdigit() or not (1 <= int(e_month) <= 12):
            st.error("Month must be 01-12")
        else:
            try:
                datetime.strptime(e_date, "%d-%m-%Y")
            except ValueError:
                st.error("Date format must be DD-MM-YYYY")
                st.stop()

            month_key = e_month.zfill(2)
            st.session_state.expense_records.append([month_key, e_date, e_category, e_amount])
            st.session_state.account_balance[month_key] = (
                st.session_state.account_balance.get(month_key, 0) - e_amount
            )
            save_data()
            remaining = st.session_state.account_balance[month_key]
            st.success(f"Expense Added! Remaining Balance: ₹{remaining}")

# ======================== CHART TAB ========================
with tabs[3]:
    st.subheader("Expense Distribution by Category")
    if not st.session_state.expense_records:
        st.warning("No expense data available yet.")
    else:
        df = pd.DataFrame(
            st.session_state.expense_records, columns=["Month", "Date", "Category", "Amount"]
        )
        category_totals = df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Expense Distribution by Category", fontweight="bold")
        st.pyplot(fig)

# ======================== REPORT TAB ========================
with tabs[4]:
    st.subheader("Monthly Summary & Report")

    if st.session_state.expense_records:
        df_expenses = pd.DataFrame(
            st.session_state.expense_records, columns=["Month", "Date", "Category", "Amount"]
        )
    else:
        df_expenses = pd.DataFrame(columns=["Month", "Date", "Category", "Amount"])

    summary_list = []
    for month in sorted(st.session_state.monthly_income.keys()):
        total_income = sum(st.session_state.monthly_income.get(month, {}).values())
        total_budget = sum(st.session_state.monthly_budget.get(month, {}).values())
        total_expense = df_expenses[df_expenses["Month"] == month]["Amount"].sum()
        if pd.isna(total_expense):
            total_expense = 0
        net_saving = total_income - total_expense
        summary_list.append(
            {
                "Month": month,
                "Total Income": total_income,
                "Total Budget": total_budget,
                "Total Expense": int(total_expense),
                "Saving/Loss": int(net_saving),
            }
        )

    df_summary = pd.DataFrame(summary_list)
    st.dataframe(df_summary, use_container_width=True)

    if st.button("Generate Excel Report"):
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_expenses.to_excel(writer, sheet_name="Expense Details", index=False)
            df_summary.to_excel(writer, sheet_name="Monthly Summary", index=False)

        st.download_button(
            label="⬇️ Download Finance_Report.xlsx",
            data=output.getvalue(),
            file_name="Finance_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

st.caption("All data is saved automatically")
