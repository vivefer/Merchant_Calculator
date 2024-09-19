import random
import numpy as np

# Economic Parameters Initialization based on historical data
gdp = 40.83  # GDP in billions USD (2022)
inflation_rate = 7.7  # Inflation rate (2022)
unemployment_rate = 11.0  # Unemployment rate (2023)
remittance_percentage = 22.8  # Remittances as % of GDP (2022)
fdi_percentage = 0.2  # FDI as % of GDP (2022)
debt_to_gdp_ratio = 39.9  # Government debt-to-GDP ratio (2021)

# Number of years to simulate
years_to_simulate = 5

# Function to simulate the economic indicators for the given years
def simulate_economy(years):
    global gdp, inflation_rate, unemployment_rate, remittance_percentage, fdi_percentage, debt_to_gdp_ratio
    for year in range(years):
        # Simulate GDP Growth based on historical trends
        gdp_growth = np.random.normal(5.6, 1)  # Using historical average and variance
        gdp *= (1 + gdp_growth / 100)

        # Simulate Inflation
        inflation_change = np.random.normal(2, 1)  # Inflation changes randomly
        inflation_rate = max(0, inflation_rate + inflation_change)

        # Simulate Unemployment
        unemployment_change = np.random.normal(-0.5, 1)  # Unemployment usually decreases with growth
        unemployment_rate = max(0, unemployment_rate + unemployment_change)

        # Simulate Remittances as a % of GDP
        remittance_percentage_change = np.random.normal(0, 0.5)  # Slow change in remittances
        remittance_percentage += remittance_percentage_change

        # Simulate FDI as % of GDP
        fdi_change = np.random.normal(0.05, 0.1)  # FDI may grow slowly or shrink
        fdi_percentage += fdi_change

        # Simulate Debt-to-GDP Ratio
        debt_to_gdp_change = np.random.normal(0.5, 1)  # Random changes in debt
        debt_to_gdp_ratio += debt_to_gdp_change

        # Print results for each year
        print(f"Year {year + 1}:")
        print(f"GDP: {gdp:.2f} billion USD")
        print(f"Inflation: {inflation_rate:.2f}%")
        print(f"Unemployment: {unemployment_rate:.2f}%")
        print(f"Remittances: {remittance_percentage:.2f}% of GDP")
        print(f"FDI: {fdi_percentage:.2f}% of GDP")
        print(f"Debt-to-GDP Ratio: {debt_to_gdp_ratio:.2f}%\n")

# Run the simulation for 5 years
simulate_economy(years_to_simulate)
