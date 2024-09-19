import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for customers
if 'customers' not in st.session_state:
    st.session_state['customers'] = []

# Function to add customer credit details
def add_customer_credit():
    with st.form("Customer Entry Form"):
        customer_name = st.text_input("Enter customer's name:")
        amount_borrowed = st.number_input("Enter the amount borrowed:", min_value=0.0, step=0.01)
        repay_time = st.number_input("Enter the time taken to repay (in days):", min_value=1.0, step=1.0)
        
        # Submit button for entering customer details
        submitted = st.form_submit_button("Submit Customer Details")
        
        if submitted:
            credit_score = amount_borrowed / repay_time  # Credit score based on Amount/Time logic
            st.session_state['customers'].append({
                'Customer': customer_name,
                'Amount_Borrowed': amount_borrowed,
                'Repay_Time': repay_time,
                'Credit_Score': credit_score
            })
            st.write(f"Customer {customer_name}'s credit details added!")

# Function to calculate and display credit scores
def credit_analysis():
    if len(st.session_state['customers']) > 0:
        credit_data = pd.DataFrame(st.session_state['customers'])
        
        # Display customer credit data
        st.write("Customer Credit Details with Credit Scores:")
        st.dataframe(credit_data)

        # Plot Amount vs Repay Time and label Credit Score
        plt.figure(figsize=(10, 6))
        for i, row in credit_data.iterrows():
            plt.scatter(row['Repay_Time'], row['Amount_Borrowed'], label=f"{row['Customer']} (Score: {row['Credit_Score']:.2f})")
            plt.text(row['Repay_Time'] + 0.2, row['Amount_Borrowed'], row['Customer'], fontsize=9)
        
        plt.title('Amount vs Repay Time for Customers')
        plt.xlabel('Repay Time (days)')
        plt.ylabel('Amount Borrowed')
        plt.grid(True)
        plt.legend()
        
        # Display the plot
        st.pyplot(plt)

# Main function for customer credit page
def customer_credit_page():
    st.title("Customer Credit Tracking")

    # Step 1: Add customer details
    st.header("Enter Customer Credit Details")
    add_customer_credit()

    # Step 2: Button to stop customer entry and calculate credit scores
    if st.button("End Customer Entry and Calculate Credit Scores"):
        credit_analysis()

if __name__ == "__main__":
    customer_credit_page()
