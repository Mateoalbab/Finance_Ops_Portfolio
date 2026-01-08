import pandas as pd
import numpy as np
import random
from datetime import date, timedelta
import os

# ==========================================
# 🚀 PART 4: THE STANDARD DATA GENERATOR
# ==========================================
# This script generates clean, standard CSV files starting at Cell A1.
# This is the "Industry Standard" format for feeding Power BI.

print("🚀 Starting Data Generation Process...")

# 1. SETUP FOLDERS
# ------------------------------------------
# We save data to the '02_Data' folder.
output_folder = "../02_Data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 2. CREATE DIMENSION TABLE (Chart of Accounts)
# ------------------------------------------
# This table defines "What" we are spending money on.
accounts_data = {
    'Account_ID': [101, 102, 201, 202, 301, 302, 303, 304],
    'Account_Name': [
        'Service Revenue', 'Logistics Fees',       # Revenue (Money In)
        'Fuel Costs', 'Driver Wages',              # COGS (Direct Costs)
        'HQ Salaries', 'Marketing', 'IT Software', 'Rent & Utilities'  # OPEX (Overhead)
    ],
    'Category': ['Revenue', 'Revenue', 'COGS', 'COGS', 'OPEX', 'OPEX', 'OPEX', 'OPEX'],
    'Sub_Category': ['Sales', 'Fees', 'Variable', 'Variable', 'Fixed', 'Fixed', 'Fixed', 'Fixed']
}

df_accounts = pd.DataFrame(accounts_data)

# 3. CREATE FACT TABLE (Transactions)
# ------------------------------------------
# We simulate 24 months of data (2024-2025).

start_date = date(2024, 1, 1)
days_range = 730  # 2 years
regions = ['NAM', 'LATAM', 'EMEA', 'APAC']
scenarios = ['Actual', 'Budget']

rows = 20000
data = []

print(f"⚙️ Generating {rows} rows of financial transactions...")

for _ in range(rows):
    # A. Date Logic
    random_days = random.randint(0, days_range)
    txn_date = start_date + timedelta(days=random_days)
    txn_date = txn_date.replace(day=1) # Finance data is usually monthly (1st of month)

    # B. Context Logic
    region = random.choice(regions)
    account = random.choice(accounts_data['Account_ID'])
    scenario = random.choice(scenarios)

    # C. Money Logic
    base_amount = random.randint(5000, 50000)
    
    # Variance Logic: Actuals are "messy", Budget is "clean"
    if scenario == 'Actual':
        # Add random noise (+/- 15%)
        amount = base_amount * random.uniform(0.85, 1.15)
    else:
        amount = base_amount

    # Sign Logic: Expenses are Negative (-), Revenue is Positive (+)
    if account > 200: 
        amount = amount * -1

    data.append([txn_date, region, account, scenario, round(amount, 2)])

df_financials = pd.DataFrame(data, columns=['Date', 'Region', 'Account_ID', 'Scenario', 'Amount'])

# 4. EXPORT TO CSV (Standard Format)
# ------------------------------------------
# index=False means "Don't print the row numbers (0, 1, 2...)", just the data.

file_accounts = f"{output_folder}/dim_accounts.csv"
file_financials = f"{output_folder}/fact_financials.csv"

print("💾 Saving to CSV...")

df_accounts.to_csv(file_accounts, index=False)
df_financials.to_csv(file_financials, index=False)

print("✅ SUCCESS! Two clean files created in '/02_Data':")
print(f"   1. {file_accounts}")
print(f"   2. {file_financials}")