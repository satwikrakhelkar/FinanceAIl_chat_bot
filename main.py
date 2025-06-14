import streamlit as st
import requests
import json
import time
from datetime import datetime

# Streamlit configuration
st.set_page_config(
    page_title="FinanceMate - Your Personal Financial Assistant",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
    }
    .message-content {
        color: #666;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "budget" not in st.session_state:
    st.session_state.budget = {}
if "expenses" not in st.session_state:
    st.session_state.expenses = {}

# Function to add a new budget category
def add_budget():
    category = st.text_input("Enter a new budget category:", key="new_category")
    amount = st.number_input(f"Set budget for {category} (INR):", min_value=0.0, key="new_amount")
    if st.button("Add Budget", key="add_budget"):
        if category and amount:
            st.session_state.budget[category] = amount
            st.success(f"Budget added: {category} - INR {amount}")
        else:
            st.error("Please enter a valid category and amount.")

# Function to log an expense
def log_expense():
    category = st.selectbox("Select a category:", options=list(st.session_state.budget.keys()), key="expense_category")
    amount = st.number_input("Enter expense amount (INR):", min_value=0.0, key="expense_amount")
    date = st.date_input("Select expense date:", key="expense_date")
    if st.button("Log Expense", key="log_expense"):
        if category and amount:
            if category not in st.session_state.expenses:
                st.session_state.expenses[category] = []
            st.session_state.expenses[category].append({"amount": amount, "date": date.strftime('%Y-%m-%d')})
            st.success(f"Expense logged: {category} - INR {amount} on {date}")
        else:
            st.error("Please enter a valid category and amount.")

# Function to generate the balance sheet
def generate_balance_sheet():
    st.header("📊 Monthly Balance Sheet")
    total_budget = sum(st.session_state.budget.values())
    total_expenses = sum(
        expense["amount"] for expenses in st.session_state.expenses.values() for expense in expenses
    )
    st.subheader(f"Total Budget: INR {total_budget}")
    st.subheader(f"Total Expenses: INR {total_expenses}")
    st.subheader(f"Remaining Balance: INR {total_budget - total_expenses}")

    # Display category-wise breakdown
    for category, amount in st.session_state.budget.items():
        expenses_in_category = sum(
            expense["amount"] for expense in st.session_state.expenses.get(category, [])
        )
        st.write(f"**{category}:** Budgeted: INR {amount}, Spent: INR {expenses_in_category}, Remaining: INR {amount - expenses_in_category}")

# Chat assistant function
def format_message(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">👤 You</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-header">💵 FinanceMate</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.title("💵 FinanceMate - Personal Financial Assistant")
    st.markdown("Your AI-powered assistant for better money health and financial planning.")

    # Sidebar menu
    with st.sidebar:
        st.header("🏦 Financial Tools")
        st.subheader("💰 Budget Planner")
        add_budget()

        st.subheader("💸 Expense Logger")
        log_expense()

        st.markdown("---")
        if st.button("📊 Generate Balance Sheet"):
            st.session_state.show_balance_sheet = True

    # Chat area
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            format_message(message["role"], message["content"])

    # User input for chat
    user_input = st.chat_input("Type your question or request here...")
    if user_input:
        # Add user message to session
        st.session_state.messages.append({"role": "user", "content": user_input})
        format_message("user", user_input)

        # FinanceMate response
        response = """I am here to help with:
        
- Setting budgets for different categories.
- Logging expenses to track spending.
- Providing a monthly balance sheet with insights.
- Suggestions for better money management.

What would you like assistance with?"""
        st.session_state.messages.append({"role": "assistant", "content": response})
        format_message("assistant", response)

    # Generate balance sheet if requested
    if st.session_state.get("show_balance_sheet", False):
        generate_balance_sheet()

if __name__ == "__main__":
    main()
