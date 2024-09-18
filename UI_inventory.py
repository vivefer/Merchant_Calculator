import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS and JavaScript for arrow key navigation
st.markdown("""
    <style>
        input {
            font-size: 18px;
            padding: 5px;
        }
        button {
            font-size: 18px;
            padding: 10px;
        }
    </style>
    
    <script>
        document.addEventListener("keydown", function(event) {
            const inputs = document.querySelectorAll("input");
            let currentIndex = [...inputs].indexOf(document.activeElement);
            
            if (event.key === "ArrowDown" || event.key === "ArrowRight") {
                if (currentIndex + 1 < inputs.length) {
                    inputs[currentIndex + 1].focus();
                }
            } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
                if (currentIndex > 0) {
                    inputs[currentIndex - 1].focus();
                }
            }
        });
    </script>
""", unsafe_allow_html=True)

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

st.title("Product Sales and Profit Tracker")

# Step 1: Input for the list of products
st.header("Enter Product Information")

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
        # Store products in session state
        st.session_state['products'] = products
        st.session_state['cost_price'] = cost_price
        st.session_state['selling_price'] = selling_price
        
        # Initialize times sold for each product
        st.session_state['times_sold'] = [0] * num_products
        st.session_state['selling_active'] = True
        st.write("Product details submitted!")

# Step 2: Continuous Selling Phase
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
        # Step 3: Calculate profit per product
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

        # Step 4: Calculate selling rate for each product (based on times sold)
        data['Selling_rate'] = data['Times_Sold']

        # Step 5: Calculate Profit x Selling Rate
        data['Profit_x_Selling_rate'] = data['Profit_per_product'] * data['Selling_rate']

        # Step 6: Classify products based on profit and selling rate
        def classify_product(row):
            if row['Profit_per_product'] > row['Selling_rate']:
                return 'Focus on Selling'
            elif row['Selling_rate'] > row['Profit_per_product']:
                return 'Focus on Stocking'
            else:
                return 'High Stock and Sell Priority'

        data['Strategy'] = data.apply(classify_product, axis=1)

        st.session_state['data'] = data

# Step 7: Display Results
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

    # Step 8: Display classification and strategy
    st.subheader("All Products with their Profit x Selling Rate and Strategy")
    st.dataframe(st.session_state['data'][['Product', 'Cost_Price', 'Selling_Price', 'Profit_per_product', 'Times_Sold', 'Profit_x_Selling_rate', 'Strategy']])
