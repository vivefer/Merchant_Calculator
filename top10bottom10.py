import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulating data for a month with 50 products typical of a Nepali grocery store
np.random.seed(42)

# List of 50 typical Nepali grocery and departmental store products
products = [
    'Rice', 'Lentils', 'Flour', 'Sugar', 'Salt', 'Cooking Oil', 'Tea', 'Milk Powder', 'Ghee', 'Spices',
    'Biscuits', 'Instant Noodles', 'Bottled Water', 'Cold Drinks', 'Snacks', 'Bread', 'Eggs', 'Butter', 'Cheese', 'Yogurt',
    'Toothpaste', 'Shampoo', 'Soap', 'Detergent', 'Dishwash', 'Toilet Paper', 'Tissues', 'Hand Wash', 'Sanitary Pads', 'Diapers',
    'Shaving Cream', 'Razors', 'Face Cream', 'Hair Oil', 'Hair Gel', 'Perfume', 'Deodorant', 'Batteries', 'Light Bulbs', 'Matches',
    'Mosquito Coil', 'Insect Spray', 'Dettol', 'First Aid Kit', 'Pain Relievers', 'Vitamins', 'Cough Syrup', 'Thermometer', 'Masks', 'Gloves'
]

# Simulate profit and selling rate
profit = np.random.uniform(10, 100, size=50)  # profit per product (in arbitrary units)
selling_rate = np.random.uniform(50, 500, size=50)  # selling rate (number of items sold per month)

# Multiply selling rate and profit to sort products
profit_x_selling_rate = profit * selling_rate

# Create DataFrame
data = pd.DataFrame({
    'Product': products,
    'Profit_per_product': profit,
    'Selling_rate': selling_rate,
    'Profit_x_Selling_rate': profit_x_selling_rate
})

# Sort by the product of profit and selling rate
data_sorted = data.sort_values(by='Profit_x_Selling_rate', ascending=False).reset_index(drop=True)

# Define categories based on the graph logic
def classify_product(row):
    if row['Profit_per_product'] > row['Selling_rate']:
        return 'Focus on Selling'
    elif row['Selling_rate'] > row['Profit_per_product']:
        return 'Focus on Stocking'
    else:
        return 'High Stock and Sell Priority'

# Classify products based on selling rate and profit deviation
data_sorted['Strategy'] = data_sorted.apply(classify_product, axis=1)

# Plotting Profit vs Selling Rate
plt.figure(figsize=(10, 8))
plt.scatter(data_sorted['Profit_per_product'], data_sorted['Selling_rate'], color='g')

# Adding labels for products with the highest and lowest profit x selling rate
for i in range(len(data_sorted)):
    if i < 5 or i > 45:  # Show only for top and bottom 5 products
        plt.text(data_sorted['Profit_per_product'][i] + 0.5, data_sorted['Selling_rate'][i],
                 data_sorted['Product'][i], fontsize=8)

plt.title('Profit vs Selling Rate for Nepali Grocery Store Products')
plt.xlabel('Profit per Product')
plt.ylabel('Selling Rate')
plt.grid(True)
plt.show()

# Print the sorted data with classification
print("Top 10 Products by Profit x Selling Rate:")
print(data_sorted[['Product', 'Profit_per_product', 'Selling_rate', 'Profit_x_Selling_rate', 'Strategy']].head(10))

print("\nBottom 10 Products by Profit x Selling Rate:")
print(data_sorted[['Product', 'Profit_per_product', 'Selling_rate', 'Profit_x_Selling_rate', 'Strategy']].tail(10))
