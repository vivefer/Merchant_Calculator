import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Initialize session state
if 'products' not in st.session_state:
    st.session_state['products'] = []
if 'cost_price' not in st.session_state:
    st.session_state['cost_price'] = []
if 'selling_price' not in st.session_state:
    st.session_state['selling_price'] = []
if 'times_sold' not in st.session_state:
    st.session_state['times_sold'] = []
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()
if 'selling_active' not in st.session_state:
    st.session_state['selling_active'] = False

# File paths for storing data
product_file = 'products.csv'
stats_file = 'stats.csv'
time_log_file = 'time_log.csv'

# Helper functions to load/save data
def load_csv(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        return pd.DataFrame()

def save_csv(data, file):
    data.to_csv(file, index=False)

def update_time_log(custom_interval=None):
    now = datetime.now()
    if custom_interval:
        next_update = now + timedelta(days=custom_interval)
    else:
        next_update = now
    log_data = pd.DataFrame({'Last_Update': [now], 'Next_Update': [next_update]})
    save_csv(log_data, time_log_file)

# Load data from previous sessions
product_data = load_csv(product_file)
stats_data = load_csv(stats_file)
time_log = load_csv(time_log_file)

# Check if it's time to update (based on time log)
if not time_log.empty:
    last_update = pd.to_datetime(time_log['Last_Update'].iloc[-1])
    next_update = pd.to_datetime(time_log['Next_Update'].iloc[-1])
else:
    last_update = datetime.now()
    next_update = datetime.now()

def input_page():
    st.title("Product Sales and Profit Tracker - Product Input")
    st.write(f"Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Next Update Scheduled: {next_update.strftime('%Y-%m-%d %H:%M:%S')}")

    num_products = st.number_input("Enter the number of products:", min_value=1, step=1)

    with st.form("Product Entry Form"):
        products = []
        cost_price = []
        selling_price = []
        
        for i in range(num_products):
            st.write(f"Product {i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                product_name = st.text_input(f"Product {i+1} Name:", key=f'product_name_{i}')
                products.append(product_name)
            with col2:
                cp = st.number_input(f"Cost Price of {product_name}:", min_value=0.0, step=0.01, key=f'cp_{i}')
                cost_price.append(cp)
            with col3:
                sp = st.number_input(f"Selling Price of {product_name}:", min_value=0.0, step=0.01, key=f'sp_{i}')
                selling_price.append(sp)

        submitted = st.form_submit_button("Submit Products")
        
        if submitted:
            # Store products in session state and save to file
            st.session_state['products'] = products
            st.session_state['cost_price'] = cost_price
            st.session_state['selling_price'] = selling_price
            product_df = pd.DataFrame({
                'Product': products,
                'Cost_Price': cost_price,
                'Selling_Price': selling_price
            })
            save_csv(product_df, product_file)
            
            # Initialize times sold for each product
            st.session_state['times_sold'] = [0] * num_products
            st.session_state['selling_active'] = True
            st.write("Product details submitted and saved!")

def sales_page():
    st.title("Product Sales and Profit Tracker - Sales Tracking")

    if len(st.session_state['products']) > 0 and st.session_state['selling_active']:
        st.header("Sell Products")
        st.write("Keep selecting products to sell. Click 'Exit' when you're done.")

        col1, col2 = st.columns([2, 1])
        with col1:
            sold_product = st.selectbox("Choose a product being sold:", options=st.session_state['products'])

        with col2:
            if st.button("Sell Product"):
                product_index = st.session_state['products'].index(sold_product)
                st.session_state['times_sold'][product_index] += 1
                st.write(f"{sold_product} sold! Current count: {st.session_state['times_sold'][product_index]}")

        # Exit button to calculate stats
        if st.button("Exit Selling"):
            st.session_state['selling_active'] = False
            # Calculate profit per product
            profit_per_product = [
                sp - cp for sp, cp in zip(st.session_state['selling_price'], st.session_state['cost_price'])
            ]

            # Create a DataFrame to store product data
            data = pd.DataFrame({
                'Product': st.session_state['products'],
                'Cost_Price': st.session_state['cost_price'],
                'Selling_Price': st.session_state['selling_price'],
                'Profit_per_product': profit_per_product,
                'Times_Sold': st.session_state['times_sold'],
            })

            # Calculate selling rate for each product (based on times sold)
            data['Selling_rate'] = data['Times_Sold']

            # Calculate Profit x Selling Rate
            data['Profit_x_Selling_rate'] = data['Profit_per_product'] * data['Selling_rate']

            # Classify products based on profit and selling rate
            def classify_product(row):
                if row['Profit_per_product'] > row['Selling_rate']:
                    return 'Focus on Selling'
                elif row['Selling_rate'] > row['Profit_per_product']:
                    return 'Focus on Stocking'
                else:
                    return 'High Stock and Sell Priority'

            data['Strategy'] = data.apply(classify_product, axis=1)

            # Save stats to file
            save_csv(data, stats_file)
            st.session_state['data'] = data

    if 'data' in st.session_state and not st.session_state['data'].empty:
        st.header("Profit vs Selling Rate for Products")
        
        fig, ax = plt.subplots()
        ax.scatter(st.session_state['data']['Profit_per_product'], st.session_state['data']['Selling_rate'], color='g')

        for i in range(len(st.session_state['data'])):
            ax.text(st.session_state['data']['Profit_per_product'][i] + 0.5, st.session_state['data']['Selling_rate'][i], st.session_state['data']['Product'][i], fontsize=8)

        ax.set_title('Profit vs Selling Rate for Products')
        ax.set_xlabel('Profit per Product')
        ax.set_ylabel('Selling Rate')
        ax.grid(True)

        st.pyplot(fig)

        # Display classification and strategy
        st.subheader("All Products with their Profit x Selling Rate and Strategy")
        st.dataframe(st.session_state['data'][['Product', 'Cost_Price', 'Selling_Price', 'Profit_per_product', 'Times_Sold', 'Profit_x_Selling_rate', 'Strategy']])

    # Custom Time Intervals
    st.sidebar.header("Set Custom Time Interval")
    interval_type = st.sidebar.selectbox("Select Interval Type", ['Week', 'Month', '6 Months', 'Year', 'Custom'])
    if interval_type == 'Custom':
        custom_days = st.sidebar.number_input("Enter the number of days for the custom interval:", min_value=1)
        if st.sidebar.button("Set Custom Interval"):
            update_time_log(custom_interval=custom_days)
            st.sidebar.write(f"Next Update in {custom_days} days.")
    else:
        intervals = {'Week': 7, 'Month': 30, '6 Months': 180, 'Year': 365}
        if st.sidebar.button(f"Set {interval_type} Interval"):
            update_time_log(custom_interval=intervals[interval_type])
            st.sidebar.write(f"Next Update in {intervals[interval_type]} days.")

# Main function to control page navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a Page", ["Product Input", "Sales Tracking"])
    
    if page == "Product Input":
        input_page()
    elif page == "Sales Tracking":
        sales_page()

if __name__ == "__main__":
    main()
