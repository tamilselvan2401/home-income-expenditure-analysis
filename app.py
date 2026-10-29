import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Home Finance Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏠 Home Income & Expenditure Analysis")
st.info(
    "This dashboard helps users track daily income, "
    "monitor expenses, analyse savings, and manage monthly budgets."
)
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Income & Expense",
        "Monthly Analysis",
        "Yearly Analysis",
        "Budget Tracking",
        "Savings Analysis"
    ]
)

st.subheader(menu)


st.subheader("Daily Income and Expense Entry")

entry_type = st.selectbox(
    "Select Entry Type",
    ["Income", "Expense"]
)

date = st.date_input("Select Date")

if entry_type == "Income":

    category = st.selectbox(
        "Select Income Category",
        ["Salary", "Business", "Freelancing",
         "Investments", "Rental Income", "Other"]
    )

else:

    category = st.selectbox(
        "Select Expense Category",
        ["Food", "Travel", "Shopping",
         "Bills", "Education", "Healthcare",
         "Entertainment", "Other"]
    )
amount = st.number_input(
    "Enter Amount (₹)",
    min_value=0.0
)

description = st.text_input("Enter Description")

if st.button("Submit"):

    if amount > 0:

        new_entry = pd.DataFrame([{
            "Type": entry_type,
            "Date": str(date),
            "Category": category,
            "Amount": amount,
            "Description": description
        }])

        file_name = "income_expense.csv"

        if os.path.exists(file_name):
            old_data = pd.read_csv(file_name)
            new_entry = pd.concat(
                [old_data, new_entry],
                ignore_index=True
            )

        new_entry.to_csv(file_name, index=False)

        st.success("Entry saved successfully!")

    else:
        st.warning("Please enter an amount greater than zero.")

st.subheader("Saved Income and Expense Records")

if os.path.exists("income_expense.csv"):
    data = pd.read_csv("income_expense.csv")
    st.dataframe(data, use_container_width=True)


else:
    st.info("No records found.")

st.subheader("Financial Summary")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    total_income = data[data["Type"] == "Income"]["Amount"].sum()

    total_expense = data[data["Type"] == "Expense"]["Amount"].sum()

    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹{total_income:,.2f}")

    col2.metric("Total Expense", f"₹{total_expense:,.2f}")

    col3.metric("Remaining Balance", f"₹{balance:,.2f}")

st.subheader("Monthly Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    selected_month = st.selectbox(
        "Select Month",
        range(1, 13),
        format_func=lambda x: pd.Timestamp(
            2026, x, 1
        ).strftime("%B")
    )

    selected_year = st.number_input(
        "Select Year",
        min_value=2000,
        max_value=2100,
        value=2026
    )

    monthly_data = data[
        (data["Date"].dt.month == selected_month) &
        (data["Date"].dt.year == selected_year)
    ]

    monthly_income = monthly_data[
        monthly_data["Type"] == "Income"
    ]["Amount"].sum()

    monthly_expense = monthly_data[
        monthly_data["Type"] == "Expense"
    ]["Amount"].sum()

    st.write("Monthly Income: ₹", monthly_income)
    st.write("Monthly Expense: ₹", monthly_expense)
    st.write("Monthly Savings: ₹", monthly_income - monthly_expense)

st.subheader("Yearly Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    selected_year = st.number_input(
        "Select Analysis Year",
        min_value=2000,
        max_value=2100,
        value=2026,
        key="yearly_analysis"
    )

    yearly_data = data[
        data["Date"].dt.year == selected_year
    ]

    yearly_income = yearly_data[
        yearly_data["Type"] == "Income"
    ]["Amount"].sum()

    yearly_expense = yearly_data[
        yearly_data["Type"] == "Expense"
    ]["Amount"].sum()

    yearly_savings = yearly_income - yearly_expense

    st.write("Yearly Income: ₹", yearly_income)
    st.write("Yearly Expense: ₹", yearly_expense)
    st.write("Yearly Savings: ₹", yearly_savings)

st.subheader("Category-Wise Expense Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    expense_data = data[
        data["Type"] == "Expense"
    ]

    if not expense_data.empty:

        category_expense = expense_data.groupby(
            "Category"
        )["Amount"].sum()

        st.bar_chart(category_expense)

    else:
        st.info("No expense records available yet.")

st.subheader("Expense Distribution")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    expense_data = data[
        data["Type"] == "Expense"
    ]

    if not expense_data.empty:

        category_expense = expense_data.groupby(
            "Category"
        )["Amount"].sum()

        st.write("Expense distribution by category")

        st.plotly_chart(
            __import__("plotly.express").express.pie(
                names=category_expense.index,
                values=category_expense.values,
                title="Household Expense Distribution"
            ),
            use_container_width=True
        )

    else:
        st.info("Add expense records to view the pie chart.")

import plotly.express as px

st.subheader("Monthly Income vs Expense Comparison")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    data["Month"] = data["Date"].dt.strftime("%Y-%m")

    monthly_summary = data.groupby(
        ["Month", "Type"], as_index=False
    )["Amount"].sum()

    if not monthly_summary.empty:

        fig = px.bar(
            monthly_summary,
            x="Month",
            y="Amount",
            color="Type",
            barmode="group",
            title="Monthly Income vs Expenses"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.subheader("Monthly Budget Tracking")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    budget = st.number_input(
        "Set Your Monthly Budget (₹)",
        min_value=0.0,
        value=20000.0
    )

    today = pd.Timestamp.today()

    current_month_expenses = data[
        (data["Type"] == "Expense") &
        (data["Date"].dt.month == today.month) &
        (data["Date"].dt.year == today.year)
    ]["Amount"].sum()

    st.write("Monthly Budget: ₹", budget)
    st.write("Amount Spent: ₹", current_month_expenses)

    if budget > 0:

        remaining = budget - current_month_expenses

        st.write("Remaining Budget: ₹", remaining)

        progress = min(current_month_expenses / budget, 1.0)

        st.progress(progress)

        if remaining < 0:
            st.error("You have exceeded your monthly budget!")
        else:
            st.success("You are within your monthly budget!")

st.subheader("Monthly Savings Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    data["Month"] = data["Date"].dt.strftime("%Y-%m")

    monthly_income = data[
        data["Type"] == "Income"
    ].groupby("Month")["Amount"].sum()

    monthly_expense = data[
        data["Type"] == "Expense"
    ].groupby("Month")["Amount"].sum()

    savings = monthly_income.subtract(
        monthly_expense, fill_value=0
    )

    st.write("Monthly Savings Details")

    st.dataframe(
        savings.rename("Savings Amount (₹)")
    )

    st.bar_chart(savings)

st.subheader("Download Financial Records")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Income and Expense Report",
        data=csv_data,
        file_name="Home_Financial_Report.csv",
        mime="text/csv"
    )

    st.success("Your financial report is ready to download!")

else:
    st.info("No financial records available.")

st.sidebar.title("Home Finance Dashboard")

st.sidebar.write("Welcome to our project!")

st.sidebar.markdown("---")

st.sidebar.subheader("Project Information")

st.sidebar.write("Project: Home Income and Expenditure Analysis")

st.sidebar.write("Technology: Python")

st.sidebar.write("Framework: Streamlit")

st.sidebar.write("Data Analysis: Pandas")

st.sidebar.markdown("---")

st.sidebar.info(
    "Track your income, expenses and savings easily."
)


st.subheader("Date-Wise Transaction Filter")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    start_date = st.date_input("Start Date")

    end_date = st.date_input("End Date")

    filtered_data = data[
        (data["Date"].dt.date >= start_date) &
        (data["Date"].dt.date <= end_date)
    ]

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

    st.write("Total Records:", len(filtered_data))

else:
    st.info("No records available.")


st.subheader("Highest Expense Category")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    expense_data = data[
        data["Type"] == "Expense"
    ]

    if not expense_data.empty:

        category_total = expense_data.groupby(
            "Category"
        )["Amount"].sum()

        highest_category = category_total.idxmax()

        highest_amount = category_total.max()

        st.success(
            f"Highest Spending Category: {highest_category}"
        )

        st.metric(
            "Total Amount Spent",
            f"₹{highest_amount:,.2f}"
        )

    else:
        st.info("No expense records available.")


st.subheader("Savings Percentage Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    total_income = data[
        data["Type"] == "Income"
    ]["Amount"].sum()

    total_expense = data[
        data["Type"] == "Expense"
    ]["Amount"].sum()

    savings = total_income - total_expense

    if total_income > 0:

        savings_percentage = (
            savings / total_income
        ) * 100

        st.metric(
            "Savings Percentage",
            f"{savings_percentage:.2f}%"
        )

        st.write(
            "Your savings compared to your total income."
        )

    else:
        st.info("Add income records to calculate savings percentage.")


st.subheader("Category-Wise Income Analysis")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    income_data = data[
        data["Type"] == "Income"
    ]

    if not income_data.empty:

        income_category = income_data.groupby(
            "Category"
        )["Amount"].sum()

        st.bar_chart(income_category)

    else:
        st.info("No income records available.")


st.subheader("Financial Health Status")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    total_income = data[
        data["Type"] == "Income"
    ]["Amount"].sum()

    total_expense = data[
        data["Type"] == "Expense"
    ]["Amount"].sum()

    if total_income > 0:

        savings = total_income - total_expense

        if savings > 0:
            st.success(
                "Good! Your household is saving money."
            )

        elif savings == 0:
            st.warning(
                "Your income and expenses are equal."
            )

        else:
            st.error(
                "Warning! Your expenses are higher than your income."
            )

    else:
        st.info("Add income records to check financial health.")


st.subheader("Expense Alert System")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    today = pd.Timestamp.today()

    monthly_expenses = data[
        (data["Type"] == "Expense") &
        (data["Date"].dt.month == today.month) &
        (data["Date"].dt.year == today.year)
    ]["Amount"].sum()

    monthly_budget = 20000

    st.write("Monthly Budget: ₹", monthly_budget)

    st.write("Current Expenses: ₹", monthly_expenses)

    if monthly_expenses > monthly_budget:

        st.error(
            "Alert! Your monthly expenses have exceeded the budget!"
        )

    elif monthly_expenses == monthly_budget:

        st.warning(
            "Warning! You have reached your monthly budget."
        )

    else:

        st.success(
            "Your expenses are within the monthly budget."
        )


st.subheader("Transaction Search")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    search_type = st.selectbox(
        "Search Transaction Type",
        ["All", "Income", "Expense"]
    )

    if search_type == "Income":
        filtered_data = data[
            data["Type"] == "Income"
        ]

    elif search_type == "Expense":
        filtered_data = data[
            data["Type"] == "Expense"
        ]

    else:
        filtered_data = data

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

    st.write("Total Transactions:", len(filtered_data))

else:
    st.info("No transactions available.")


st.subheader("Search by Category")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    categories = ["All"] + sorted(
        data["Category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "Select Category to Search",
        categories
    )

    if selected_category == "All":
        category_data = data
    else:
        category_data = data[
            data["Category"] == selected_category
        ]

    st.dataframe(
        category_data,
        use_container_width=True
    )

    st.write("Matching Records:", len(category_data))


st.subheader("Recent Transactions")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    recent_data = data.sort_values(
        by="Date",
        ascending=False
    ).head(5)

    st.dataframe(
        recent_data,
        use_container_width=True
    )

    st.write(
        "Showing the latest 5 transactions."
    )

else:
    st.info("No transactions available.")


st.subheader("Average Monthly Expense")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    today = pd.Timestamp.today()

    monthly_expenses = data[
        (data["Type"] == "Expense") &
        (data["Date"].dt.month == today.month) &
        (data["Date"].dt.year == today.year)
    ]

    if not monthly_expenses.empty:

        average_expense = monthly_expenses[
            "Amount"
        ].mean()

        st.metric(
            "Average Expense per Transaction",
            f"₹{average_expense:,.2f}"
        )

    else:
        st.info("No expenses recorded this month.")


st.subheader("Monthly Expense Trend")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    expense_data = data[
        data["Type"] == "Expense"
    ].copy()

    if not expense_data.empty:

        expense_data["Month"] = (
            expense_data["Date"].dt.strftime("%Y-%m")
        )

        monthly_expenses = expense_data.groupby(
            "Month"
        )["Amount"].sum().reset_index()

        st.line_chart(
            monthly_expenses.set_index("Month")
        )

    else:
        st.info("No expense records available.")


st.subheader("Delete Transaction")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    if not data.empty:

        delete_options = {
            f"{i} | {row['Date']} | {row['Type']} | {row['Category']} | ₹{row['Amount']}": i
            for i, row in data.iterrows()
        }

        selected_transaction = st.selectbox(
            "Select Transaction to Delete",
            list(delete_options.keys())
        )

        if st.button("Delete Selected Transaction"):

            row_index = delete_options[selected_transaction]

            data = data.drop(index=row_index)

            data.to_csv("income_expense.csv", index=False)

            st.success("Transaction deleted successfully!")

            st.rerun()

    else:
        st.info("No transactions available.")

else:
    st.info("No transaction file found.")


st.subheader("Edit Transaction")

if os.path.exists("income_expense.csv"):

    data = pd.read_csv("income_expense.csv")

    if not data.empty:

        transaction_options = {
            f"{i} | {row['Date']} | {row['Type']} | {row['Category']} | ₹{row['Amount']}": i
            for i, row in data.iterrows()
        }

        selected = st.selectbox(
            "Select Transaction to Edit",
            list(transaction_options.keys()),
            key="edit_transaction"
        )

        row_index = transaction_options[selected]

        st.write("Update Transaction Details")

        new_amount = st.number_input(
            "New Amount (₹)",
            min_value=0.0,
            value=float(data.loc[row_index, "Amount"]),
            key="edit_amount"
        )

        new_description = st.text_input(
            "New Description",
            value=str(data.loc[row_index, "Description"]),
            key="edit_description"
        )

        if st.button("Update Transaction"):

            if new_amount > 0:

                data.loc[row_index, "Amount"] = new_amount

                data.loc[row_index, "Description"] = new_description

                data.to_csv("income_expense.csv", index=False)

                st.success("Transaction updated successfully!")

                st.rerun()

            else:
                st.warning("Amount must be greater than zero.")

    else:
        st.info("No transactions available.")

else:
    st.info("No transaction file found.")


import io

if os.path.exists("income_expense.csv"):

    excel_data = pd.read_csv("income_expense.csv")

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        excel_data.to_excel(
            writer,
            index=False,
            sheet_name="Transactions"
        )

    st.download_button(
        label="Download Excel Report",
        data=excel_buffer.getvalue(),
        file_name="income_expense_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("No transaction records available for Excel download.")


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

pdf_buffer = io.BytesIO()

if os.path.exists("income_expense.csv"):

    pdf_data = pd.read_csv("income_expense.csv")

    pdf_doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("Home Income and Expenditure Report", styles["Title"])
    )
    elements.append(Spacer(1, 20))

    table_data = [pdf_data.columns.tolist()] + pdf_data.values.tolist()

    pdf_table = Table(table_data, repeatRows=1)

    pdf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    elements.append(pdf_table)

    pdf_doc.build(elements)

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer.getvalue(),
        file_name="income_expense_report.pdf",
        mime="application/pdf"
    )