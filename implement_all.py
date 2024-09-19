import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Input for the list of products
num_products = int(input("Enter the number of products: "))
products = []

for i in range(num_products):
    product_name = input(f"Enter the name of product {i+1}: ")
    products.append(product_name)

# Step 2: Input for cost price and selling price for each product
cost_price = []
selling_price = []
for i in range(num_products):
    cp = float(input(f"Enter the cost price of {products[i]}: "))
    sp = float(input(f"Enter the selling price of {products[i]}: "))
    cost_price.append(cp)
    selling_price.append(sp)

# Step 3: Calculate profit per product
profit_per_product = [sp - cp for sp, cp in zip(selling_price, cost_price)]

# Create a DataFrame to store initial product data
data = pd.DataFrame({
    'Product': products,
    'Cost_Price': cost_price,
    'Selling_Price': selling_price,
    'Profit_per_product': profit_per_product,
    'Times_Sold': [0] * num_products  # Initialize selling count
})

# Step 4: Function to display available products for sale
def display_products():
    print("\nAvailable products for sale:")
    for i, product in enumerate(data['Product']):
        print(f"{i + 1}. {product}")

# Step 5: Option to choose which products are being sold by selecting a number
def sell_product():
    display_products()
    product_sold = input("\nEnter the number of the product being sold (or type 'exit' to finish): ").strip()

    while product_sold.lower() != 'exit':
        if product_sold.isdigit():
            product_index = int(product_sold) - 1
            if 0 <= product_index < num_products:
                data.loc[product_index, 'Times_Sold'] += 1
                print(f"{data.loc[product_index, 'Product']} sold! Current count: {int(data.loc[product_index, 'Times_Sold'])}")
            else:
                print("Invalid product number. Try again.")
        else:
            print("Invalid input. Please enter a number corresponding to a product or 'exit' to finish.")
        
        display_products()  # Display the product list again after each sale
        product_sold = input("\nEnter another product number being sold (or type 'exit' to finish): ").strip()

# Step 6: Selling the products until the user stops
sell_product()

# Step 7: Calculate selling rate for each product (based on the number of times sold)
data['Selling_rate'] = data['Times_Sold']  # Here, we'll assume selling rate is based on times sold

# Step 8: Calculate Profit x Selling Rate
data['Profit_x_Selling_rate'] = data['Profit_per_product'] * data['Selling_rate']

# Step 9: Classify products based on profit and selling rate
def classify_product(row):
    if row['Profit_per_product'] > row['Selling_rate']:
        return 'Focus on Selling'
    elif row['Selling_rate'] > row['Profit_per_product']:
        return 'Focus on Stocking'
    else:
        return 'High Stock and Sell Priority'

data['Strategy'] = data.apply(classify_product, axis=1)

# Step 10: Customer credit details and credit score calculation
customers = []

def add_customer_credit():
    customer_name = input("\nEnter customer's name: ")
    amount_borrowed = float(input("Enter the amount borrowed: "))
    repay_time = float(input("Enter the time taken to repay (in days): "))
    credit_score = amount_borrowed / repay_time  # Credit score based on Amount/Time logic
    customers.append({
        'Customer': customer_name,
        'Amount_Borrowed': amount_borrowed,
        'Repay_Time': repay_time,
        'Credit_Score': credit_score
    })

def credit_analysis():
    credit_data = pd.DataFrame(customers)
    print("\nCustomer Credit Details with Credit Scores:")
    print(credit_data)

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
    plt.show()

# Step 11: Option to record customer credit details
def record_credit_sales():
    while True:
        record_credit = input("\nDo you want to record a credit sale? (yes/no): ").strip().lower()
        if record_credit == 'yes':
            add_customer_credit()
        elif record_credit == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Step 12: Display and analyze customer credit data
record_credit_sales()
credit_analysis()

# Step 13: Plotting Profit vs Selling Rate for Products
plt.figure(figsize=(10, 8))
plt.scatter(data['Profit_per_product'], data['Selling_rate'], color='g')

# Adding labels for products with the highest and lowest profit x selling rate
for i in range(len(data)):
    plt.text(data['Profit_per_product'][i] + 0.5, data['Selling_rate'][i], data['Product'][i], fontsize=8)

plt.title('Profit vs Selling Rate for Products')
plt.xlabel('Profit per Product')
plt.ylabel('Selling Rate')
plt.grid(True)
plt.show()

# Step 14: Print all products with classification
print("\nAll Products with their Profit x Selling Rate and Strategy:")
print(data[['Product', 'Cost_Price', 'Selling_Price', 'Profit_per_product', 'Times_Sold', 'Profit_x_Selling_rate', 'Strategy']])
