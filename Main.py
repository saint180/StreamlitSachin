import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Expense Advisor", layout="wide")
st.title("💰 Expense Advisor App")

# Sidebar - Income and savings input
st.sidebar.header("User Settings")
monthly_income = st.sidebar.number_input("Enter your monthly income:", min_value=0)
savings_goal = st.sidebar.number_input("Enter your monthly savings goal:", min_value=0)

# Initialize session state for data
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# Expense Entry Form
st.subheader("📋 Enter a New Expense")
with st.form("expense_form"):
    date = datetime.today().strftime("%Y-%m-%d")
    category = st.selectbox("Expense Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_entry = {"Date": date, "Category": category, "Description": description, "Amount": amount}
        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, pd.DataFrame([new_entry])], ignore_index=True
        )
        st.success("Expense added successfully!")

# Display Expense Table
st.subheader("📊 Weekly Expense Log")
st.dataframe(st.session_state.expenses, use_container_width=True)

# Budget Summary and Alert
total_expenses = st.session_state.expenses["Amount"].sum()
remaining_budget = monthly_income - savings_goal

st.markdown(f"**Total Expenses:** ₹{total_expenses:.2f}")
st.markdown(f"**Remaining Budget (Income - Savings):** ₹{remaining_budget:.2f}")

if total_expenses > remaining_budget:
    st.warning("⚠️ You have exceeded your monthly budget after savings!")
else:
    st.success("✅ You're within your budget. Keep it up!")

# Visualization - Pie Chart
st.subheader("📈 Expense Distribution by Category")
if not st.session_state.expenses.empty:
    category_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(category_data, labels=category_data.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# Visualization - Bar Chart
st.subheader("📉 Daily Expense Trend")
if not st.session_state.expenses.empty:
    daily_data = st.session_state.expenses.groupby("Date")["Amount"].sum()
    st.bar_chart(daily_data)

# Export Data to CSV
st.subheader("⬇️ Export Weekly Data")
csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
st.download_button("Download as CSV", csv, file_name="weekly_expenses.csv", mime="text/csv")
