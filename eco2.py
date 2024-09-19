import random
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Initialize historical economic data
gdp = 40.83  # GDP in billions USD (2022)
inflation_rate = 7.7  # Inflation rate (2022)
unemployment_rate = 11.0  # Unemployment rate (2023)
remittance_percentage = 22.8  # Remittances as % of GDP (2022)
fdi_percentage = 0.2  # FDI as % of GDP (2022)
debt_to_gdp_ratio = 39.9  # Government debt-to-GDP ratio (2021)
merchant_impact = 14 / 100  # Merchant software contribution to GDP

years_to_simulate = 5  # Number of years to simulate
years = list(range(1, years_to_simulate + 1))

# Lists to store the results for plotting
gdp_list = []
gdp_merchant_list = []
inflation_list = []
unemployment_list = []
remittance_list = []
fdi_list = []
debt_to_gdp_list = []

# Simulate the economy for the given number of years
for year in years:
    # Simulate GDP Growth based on historical trends (Base Case)
    gdp_growth = np.random.normal(5.6, 1)
    gdp_no_merchant = gdp * (1 + gdp_growth / 100)

    # Simulate GDP with merchant impact (14% contribution)
    gdp_with_merchant = gdp_no_merchant * (1 + merchant_impact)

    # Simulate Inflation
    inflation_change = np.random.normal(2, 1)
    inflation_rate = max(0, inflation_rate + inflation_change)

    # Simulate Unemployment
    unemployment_change = np.random.normal(-0.5, 1)
    unemployment_rate = max(0, unemployment_rate + unemployment_change)

    # Simulate Remittances as % of GDP
    remittance_percentage_change = np.random.normal(0, 0.5)
    remittance_percentage += remittance_percentage_change

    # Simulate FDI as % of GDP
    fdi_change = np.random.normal(0.05, 0.1)
    fdi_percentage += fdi_change

    # Simulate Debt-to-GDP Ratio
    debt_to_gdp_change = np.random.normal(0.5, 1)
    debt_to_gdp_ratio += debt_to_gdp_change

    # Append results to lists
    gdp_list.append(gdp_no_merchant)
    gdp_merchant_list.append(gdp_with_merchant)
    inflation_list.append(inflation_rate)
    unemployment_list.append(unemployment_rate)
    remittance_list.append(remittance_percentage)
    fdi_list.append(fdi_percentage)
    debt_to_gdp_list.append(debt_to_gdp_ratio)

# Create a DataFrame for visualization
data = pd.DataFrame({
    'Year': years,
    'GDP Without Merchant (Billion USD)': gdp_list,
    'GDP With Merchant (Billion USD)': gdp_merchant_list,
    'Inflation Rate (%)': inflation_list,
    'Unemployment Rate (%)': unemployment_list,
    'Remittances (% of GDP)': remittance_list,
    'FDI (% of GDP)': fdi_list,
    'Debt-to-GDP Ratio (%)': debt_to_gdp_list
})

# Plot using Seaborn with interactive features using Plotly
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# Plotting GDP with and without merchant software using Seaborn for static visualization
sns.lineplot(x='Year', y='GDP Without Merchant (Billion USD)', data=data, marker='o', label='GDP Without Merchant')
sns.lineplot(x='Year', y='GDP With Merchant (Billion USD)', data=data, marker='o', label='GDP With Merchant')
plt.title('GDP Growth Comparison (With and Without Merchant Software)', fontsize=16)
plt.show()

# Now we use Plotly for an interactive multi-line graph
fig = px.line(data, x='Year', y=['GDP Without Merchant (Billion USD)', 'GDP With Merchant (Billion USD)',
                                 'Inflation Rate (%)', 'Unemployment Rate (%)', 
                                 'Remittances (% of GDP)', 'FDI (% of GDP)', 'Debt-to-GDP Ratio (%)'],
              title='Economic Indicators Over Time (With and Without Merchant Software)',
              labels={'value': 'Indicator Value', 'variable': 'Economic Indicators'},
              markers=True)

# Show the interactive graph
fig.show()
